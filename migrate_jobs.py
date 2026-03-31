from datetime import datetime
from app.models import Job
from app.extension import db
from app import create_app
import sqlite3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
os.chdir(os.path.join(os.path.dirname(__file__), "backend"))


SQLITE_PATH = os.path.join("instance", "langlocaljobs.db")

app = create_app()
with app.app_context():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, description, url, posted_at FROM jobs")
    sqlite_jobs = cur.fetchall()
    conn.close()
    print(f"Found {len(sqlite_jobs)} jobs in SQLite")

    existing_urls = {
        r[0]
        for r in db.session.execute(
            db.text("SELECT url FROM jobs WHERE url IS NOT NULL")
        ).fetchall()
    }
    existing_keys = {
        r
        for r in db.session.execute(
            db.text(
                "SELECT LOWER(title), LOWER(COALESCE(company,'')), LOWER(COALESCE(location,'')) FROM jobs"
            )
        ).fetchall()
    }

    inserted = 0
    skipped = 0

    for row in sqlite_jobs:
        url = (row["url"] or "").strip()
        title = (row["title"] or "").strip()
        company = (row["company"] or "").strip()
        location = (row["location"] or "").strip()

        key = (title.lower(), company.lower(), location.lower())
        if key in existing_keys:
            skipped += 1
            continue

        posted_at = None
        if row["posted_at"]:
            try:
                posted_at = datetime.fromisoformat(str(row["posted_at"]))
            except Exception:
                posted_at = None

        job = Job(
            title=title,
            company=company or None,
            location=location or None,
            description=row["description"],
            url=url or None,
            posted_at=posted_at,
        )
        db.session.add(job)
        existing_keys.add(key)
        inserted += 1

    db.session.commit()
    total = Job.query.count()
    print(
        f"Inserted: {inserted}, Skipped (duplicates): {skipped}, Total in Postgres: {total}")
