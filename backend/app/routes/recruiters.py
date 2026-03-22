from flask import Blueprint, request, current_app
from app.extension import db
from app.models import Recruiter, User
import jwt
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return {"error": "Authentication required. Please log in or register."}, 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = payload.get("user_id")
            request.is_admin = payload.get("is_admin", False)
        except Exception:
            return {"error": "Invalid or expired token. Please log in again."}, 401
        return f(*args, **kwargs)
    return decorated


recruiters_bp = Blueprint("recruiters", __name__)


# Admin authentication decorator

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return {"error": "Admin access required."}, 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            if not payload.get("is_admin"):
                return {"error": "Admin access required."}, 403
        except Exception:
            return {"error": "Invalid or expired token."}, 401
        return f(*args, **kwargs)
    return decorated

# PATCH endpoint for recruiters to update their own details or for admin to update any recruiter


@recruiters_bp.patch("/api/recruiters/<int:recruiter_id>")
@login_required
def update_recruiter(recruiter_id):
    recruiter = Recruiter.query.get(recruiter_id)
    if not recruiter:
        return {"error": "Recruiter not found"}, 404
    data = request.get_json() or {}
    # Only allow recruiter to update their own details, unless admin
    if not request.is_admin and request.user_id != recruiter.user_id:
        return {"error": "You can only update your own recruiter profile."}, 403
    allowed_fields = ["company_name", "website"]
    updated = False
    for field in allowed_fields:
        if field in data:
            setattr(recruiter, field, data[field])
            updated = True
    if updated:
        db.session.commit()
        return {"message": f"Recruiter {recruiter_id} updated successfully."}
    else:
        return {"error": "No valid fields to update."}, 400


@recruiters_bp.get("/api/recruiters")
@admin_required
def list_recruiters():
    recruiters = Recruiter.query.order_by(Recruiter.id.desc()).all()
    return [
        {
            "id": recruiter.id,
            "user_id": recruiter.user_id,
            "company_name": recruiter.company_name,
            "website": recruiter.website,
        }
        for recruiter in recruiters
    ]


# Get recruiter by ID
@recruiters_bp.get("/api/recruiters/<int:recruiter_id>")
@admin_required
def get_recruiter(recruiter_id):
    recruiter = Recruiter.query.get(recruiter_id)
    if not recruiter:
        return {"error": "Recruiter not found"}, 404
    return {
        "id": recruiter.id,
        "user_id": recruiter.user_id,
        "company_name": recruiter.company_name,
        "website": recruiter.website,
    }


@recruiters_bp.post("/api/recruiters")
def create_recruiter():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get("user_id")
    company_name = (payload.get("company_name") or "").strip()
    website = payload.get("website")

    if not user_id or not company_name:
        return {"error": "user_id and company_name are required"}, 400

    user = User.query.get(user_id)
    if not user:
        return {"error": "user not found"}, 404

    if Recruiter.query.filter_by(user_id=user_id).first():
        return {"error": "recruiter profile already exists for this user"}, 409

    recruiter = Recruiter(user_id=user_id, company_name=company_name, website=website)
    user.is_recruiter = True
    db.session.add(recruiter)
    db.session.commit()

    return {
        "id": recruiter.id,
        "user_id": recruiter.user_id,
        "company_name": recruiter.company_name,
        "website": recruiter.website,
    }, 201
