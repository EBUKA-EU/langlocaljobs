from flask import Blueprint
from app.models import User

users_bp = Blueprint("users", __name__)


@users_bp.get("/api/users")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_recruiter": user.is_recruiter,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
        for user in users
    ]
