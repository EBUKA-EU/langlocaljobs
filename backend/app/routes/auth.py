from flask import Blueprint, request
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.extension import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/register")
def register():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    name = payload.get("name")
    is_recruiter = bool(payload.get("is_recruiter", False))

    if not email or not password:
        return {"error": "email and password are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "email already exists"}, 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        name=name,
        is_recruiter=is_recruiter,
    )
    db.session.add(user)
    db.session.commit()

    return {
        "message": "registration successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_recruiter": user.is_recruiter,
        },
    }, 201


@auth_bp.post("/api/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email or not password:
        return {"error": "email and password are required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"error": "invalid credentials"}, 401

    return {
        "message": "login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_recruiter": user.is_recruiter,
        },
    }, 200
