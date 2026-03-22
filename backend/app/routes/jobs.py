from app.models import Job
import jwt
from functools import wraps
from flask import Blueprint, request, current_app
jobs_bp = Blueprint("jobs", __name__)

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
            request.is_admin = payload.get("is_admin", False)
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


@jobs_bp.get("/api/jobs")
@login_required
def list_jobs():
    # Get pagination params from query string
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return {"error": "Invalid pagination parameters."}, 400

    query = Job.query.order_by(Job.posted_at.desc())
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
        "recruiter_id": job.recruiter_id,
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
