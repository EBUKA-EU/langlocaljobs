
from flask import Blueprint, request, current_app
from app.models import User
import jwt
from functools import wraps

users_bp = Blueprint("users", __name__)

# User authentication decorator


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

# PATCH endpoint for users to update their own details or for admin to update any user


@users_bp.patch("/api/users/<int:user_id>")
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    data = request.get_json() or {}
    # Only allow user to update their own details, unless admin
    if not request.is_admin and request.user_id != user_id:
        return {"error": "You can only update your own details."}, 403
    allowed_fields = ["name"]
    if request.is_admin:
        allowed_fields += ["is_admin", "is_recruiter"]
    updated = False
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
            updated = True
    # Allow password change (hash it)
    if "password" in data and (request.is_admin or request.user_id == user_id):
        from werkzeug.security import generate_password_hash
        user.password_hash = generate_password_hash(data["password"])
        updated = True
    if updated:
        from app.extension import db
        db.session.commit()
        return {"message": f"User {user_id} updated successfully."}
    else:
        return {"error": "No valid fields to update."}, 400


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


@users_bp.get("/api/users")
@admin_required
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_recruiter": user.is_recruiter,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
        for user in users
    ]


# Get user by ID
@users_bp.get("/api/users/<int:user_id>")
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "is_recruiter": user.is_recruiter,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
