from flask import Blueprint
from app.models import Job

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.get("/api/jobs")
def list_jobs():
    jobs = Job.query.order_by(Job.posted_at.desc()).all()
    return [
        {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "url": job.url,
            "posted_at": job.posted_at.isoformat() if job.posted_at else None,
        }
        for job in jobs
    ]
