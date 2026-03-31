from flask import Blueprint, request, current_app
from app.models import User, Profile
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta
from app.extension import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/register")
def register():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not name or not email or not password:
        return {"error": "name, email, and password are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "email already exists"}, 409

    now = datetime.utcnow()
    user = User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password),
        created_at=now
    )
    db.session.add(user)
    db.session.flush()  # get user.id before commit
    profile = Profile(
        id=user.id,
        name=name,
        role='user',
        created_at=now,
        updated_at=now
    )
    db.session.add(profile)
    db.session.commit()

    def iso_utc(dt):
        if not dt:
            return None
        return dt.replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')

    return {
        "message": "registration successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": iso_utc(user.created_at),
            "role": profile.role,
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

    now = datetime.utcnow()
    user.last_logged_in = now
    db.session.commit()

    profile = getattr(user, "profile", None)
    role = profile.role if profile else "user"

    # JWT encodes role as single source of truth
    token = jwt.encode(
        {
            "user_id": user.id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    def iso_utc(dt):
        if not dt:
            return None
        return dt.replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')

    return {
        "message": "login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": role,
            "last_logged_in": iso_utc(user.last_logged_in),
        },
        "token": token,
    }, 200


# Stateless logout endpoint (for API-first apps, frontend should delete token/cookie)
@auth_bp.post("/api/auth/logout")
def logout():
    return {"message": "logout successful"}, 200
