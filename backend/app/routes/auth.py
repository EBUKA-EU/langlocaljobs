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
        password_hash=generate_password_hash(password),
        created_at=now
    )
    db.session.add(user)
    db.session.flush()  # get user.id before commit
    profile = Profile(
        id=user.id,
        name=name,
        role='user',
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
            "created_at": iso_utc(user.created_at),
            "profile": {
                "id": profile.id,
                "name": profile.name,
                "role": profile.role,
                "updated_at": iso_utc(profile.updated_at),
            },
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

    # Update last_logged_in using direct SQL for debugging
    now = datetime.utcnow()
    db.session.execute(
        db.text('UPDATE users SET last_logged_in = :now WHERE id = :user_id'),
        {'now': now, 'user_id': user.id}
    )
    db.session.commit()
    user.last_logged_in = now

    # Generate JWT token (customize claims as needed)
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    def iso_utc(dt):
        if not dt:
            return None
        return dt.replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Fetch profile for name
    profile = getattr(user, "profile", None)
    return {
        "message": "login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "last_logged_in": iso_utc(user.last_logged_in),
            "profile": {
                "id": profile.id if profile else None,
                "name": profile.name if profile else None,
                "role": profile.role if profile else None,
                "updated_at": iso_utc(profile.updated_at) if profile and profile.updated_at else None,
            } if profile else None,
        },
        "token": token,
    }, 200


# Stateless logout endpoint (for API-first apps, frontend should delete token/cookie)
@auth_bp.post("/api/auth/logout")
def logout():
    return {"message": "logout successful"}, 200
