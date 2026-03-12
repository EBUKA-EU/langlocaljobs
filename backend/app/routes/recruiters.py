from flask import Blueprint, request
from app.extension import db
from app.models import Recruiter, User

recruiters_bp = Blueprint("recruiters", __name__)


@recruiters_bp.get("/api/recruiters")
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
