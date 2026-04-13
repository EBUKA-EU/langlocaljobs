from app.models import Job, SavedJob, AppliedJob
from app.extension import db
import jwt
from functools import wraps
from flask import Blueprint, request, current_app
jobs_bp = Blueprint("jobs", __name__)


# JWT authentication decorator
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
            request.role = payload.get("role", "user")
            request.is_admin = request.role == "admin"
        except Exception:
            return {"error": "Invalid or expired token. Please log in again."}, 401
        return f(*args, **kwargs)
    return decorated

# Admin-only decorator (for job deletion)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(request, "is_admin", False):
            return {"error": "Admin access required."}, 403
        return f(*args, **kwargs)
    return decorated


@jobs_bp.get("/api/jobs/saved")
@login_required
def list_saved_jobs():
    saved = SavedJob.query.filter_by(user_id=request.user_id).all()
    return {
        "saved_jobs": [
            {
                "id": s.job.id,
                "title": s.job.title,
                "company": s.job.company,
                "location": s.job.location,
                "url": s.job.url,
                "saved_at": s.saved_at.isoformat() if s.saved_at else None,
            }
            for s in saved if s.job
        ]
    }


@jobs_bp.post("/api/jobs/<int:job_id>/save")
@login_required
def save_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404
    existing = SavedJob.query.filter_by(user_id=request.user_id, job_id=job_id).first()
    if existing:
        return {"message": "Job already saved"}, 200
    saved = SavedJob(user_id=request.user_id, job_id=job_id)
    db.session.add(saved)
    db.session.commit()
    return {"message": "Job saved successfully"}, 201


@jobs_bp.delete("/api/jobs/<int:job_id>/save")
@login_required
def unsave_job(job_id):
    saved = SavedJob.query.filter_by(user_id=request.user_id, job_id=job_id).first()
    if not saved:
        return {"error": "Job not in saved list"}, 404
    db.session.delete(saved)
    db.session.commit()
    return {"message": "Job removed from saved list"}


@jobs_bp.get("/api/jobs/applied")
@login_required
def list_applied_jobs():
    applied = AppliedJob.query.filter_by(user_id=request.user_id).all()
    return {
        "applied_jobs": [
            {
                "id": a.job.id,
                "title": a.job.title,
                "company": a.job.company,
                "location": a.job.location,
                "url": a.job.url,
                "applied_at": a.applied_at.isoformat() if a.applied_at else None,
            }
            for a in applied if a.job
        ]
    }


@jobs_bp.post("/api/jobs/<int:job_id>/apply")
@login_required
def mark_applied(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404
    existing = AppliedJob.query.filter_by(
        user_id=request.user_id, job_id=job_id).first()
    if existing:
        return {"message": "Already marked as applied", "applied_at": existing.applied_at.isoformat()}, 200
    applied = AppliedJob(user_id=request.user_id, job_id=job_id)
    db.session.add(applied)
    db.session.commit()
    return {"message": "Marked as applied", "applied_at": applied.applied_at.isoformat()}, 201


@jobs_bp.get("/api/admin/applied-jobs")
@login_required
@admin_required
def admin_list_applied_jobs():
    from app.models import User
    rows = AppliedJob.query.order_by(AppliedJob.applied_at.desc()).all()
    return {
        "applied_jobs": [
            {
                "id": a.id,
                "user_id": a.user_id,
                "user_email": a.user.email if a.user else None,
                "user_name": a.user.name if a.user else None,
                "job_id": a.job_id,
                "job_title": a.job.title if a.job else None,
                "job_company": a.job.company if a.job else None,
                "applied_at": a.applied_at.isoformat() if a.applied_at else None,
            }
            for a in rows
        ],
        "total": len(rows),
    }


@jobs_bp.get("/api/jobs")
@login_required
def list_jobs():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return {"error": "Invalid pagination parameters."}, 400

    search = (request.args.get("search") or "").strip()
    location = (request.args.get("location") or "").strip()
    company = (request.args.get("company") or "").strip()
    date_from = (request.args.get("date_from") or "").strip()
    date_to = (request.args.get("date_to") or "").strip()

    query = Job.query
    if search:
        query = query.filter(Job.title.ilike(f"%{search}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if date_from:
        try:
            from datetime import datetime as dt
            query = query.filter(Job.posted_at >= dt.fromisoformat(date_from))
        except ValueError:
            pass
    if date_to:
        try:
            from datetime import datetime as dt
            query = query.filter(
                Job.posted_at <= dt.fromisoformat(date_to + "T23:59:59"))
        except ValueError:
            pass

    query = query.order_by(Job.posted_at.asc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    total = pagination.total

    return {
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.url,
                "posted_at": job.posted_at.isoformat() if job.posted_at else None,
            }
            for job in jobs
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }


# Get job by ID
@jobs_bp.get("/api/jobs/<int:job_id>")
@login_required
def get_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "url": job.url,
        "posted_at": job.posted_at.isoformat() if job.posted_at else None,
    }


# Delete job by ID (admin only)
# Delete job by ID (admin only)
@jobs_bp.delete("/api/jobs/<int:job_id>")
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404
    from app.extension import db
    db.session.delete(job)
    db.session.commit()
    return {"message": f"Job {job_id} deleted successfully."}


@jobs_bp.patch("/api/jobs/<int:job_id>")
@login_required
@admin_required
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404
    data = request.get_json() or {}
    allowed_fields = ["title", "company", "location",
                      "description", "url", "recruiter_id"]
    updated = False
    for field in allowed_fields:
        if field in data:
            setattr(job, field, data[field])
            updated = True
    if updated:
        from app.extension import db
        db.session.commit()
        return {"message": f"Job {job_id} updated successfully."}
    else:
        return {"error": "No valid fields to update."}, 400
