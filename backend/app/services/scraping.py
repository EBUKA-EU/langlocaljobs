import logging
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from app.extension import db
from app.models import Job

LOGGER = logging.getLogger(__name__)
REQUEST_HEADERS = {
    "User-Agent": "LangLocalJobsBot/1.0 (+https://github.com/EBUKA-EU/langlocaljobs)"}
REQUEST_TIMEOUT_SECONDS = 20


def _safe_text(value):
    return (value or "").strip()


def _canonicalize_job_url(url):
    """Normalize URLs to make duplicate and update detection more stable."""
    raw_url = _safe_text(url)
    if not raw_url:
        return ""

    parsed = urlparse(raw_url)
    path = parsed.path.rstrip("/")
    query_items = parse_qsl(parsed.query, keep_blank_values=True)

    # TranslatorsCafe links include a volatile "Jobs" parameter that changes often.
    if path.lower().endswith("selectedjob.asp"):
        query_items = [(k, v) for k, v in query_items if k.lower() == "job"]

    normalized_query = urlencode(sorted(query_items))
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            "",
            normalized_query,
            "",
        )
    )


def _normalize_job_key(title, company, location, url):
    """Fallback duplicate key when URL matching is unavailable."""
    return (
        _safe_text(title).lower(),
        _safe_text(company).lower(),
        _safe_text(location).lower(),
        _canonicalize_job_url(url),
    )


def _parse_datetime_or_now(value):
    return value if isinstance(value, datetime) else datetime.utcnow()


def _is_valid_job_payload(job_data):
    required_fields = ["title", "company", "location", "description", "url"]
    return all(_safe_text(job_data.get(field)) for field in required_fields)


def _fetch_soup(url):
    response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS,
                            headers=REQUEST_HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def _scrape_translatorscafe_listing(source_name, listing_url):
    """Scrape one TranslatorsCafe listing page and normalize records."""
    soup = _fetch_soup(listing_url)
    links = [
        link
        for link in soup.find_all("a", href=True)
        if "SelectedJob.asp?Job=" in link["href"]
    ]

    jobs = []
    skipped_invalid = 0
    for link in links:
        raw_title = _safe_text(link.get_text(" ", strip=True))
        full_url = _canonicalize_job_url(
            urljoin("https://www.translatorscafe.com", link["href"]))

        if "|" in raw_title:
            title_part, company_part = raw_title.split("|", 1)
            title = _safe_text(title_part)
            company = _safe_text(company_part)
        else:
            title = raw_title
            company = "Unknown"

        job = {
            "title": title,
            "company": company or "Unknown",
            "location": "Global",
            "description": f"Imported from {source_name}",
            "url": full_url,
            "posted_at": datetime.utcnow(),
        }

        if not _is_valid_job_payload(job):
            skipped_invalid += 1
            continue

        jobs.append(job)

    return {
        "source": source_name,
        "fetched": len(links),
        "valid": len(jobs),
        "invalid": skipped_invalid,
        "error": None,
        "jobs": jobs,
    }


def scrape_jobs_from_sources():
    """
    Scrape jobs from multiple HTML sources.
    Continues on source-level failures and returns per-source metrics.
    """
    source_configs = [
        {
            "name": "translatorscafe-selected",
            "url": "https://www.translatorscafe.com/cafe/SearchJobs.asp?Mode=Selected",
            "type": "html",
        },
        {
            "name": "translatorscafe-interpreting",
            "url": "https://www.translatorscafe.com/cafe/SearchJobs.asp?Mode=Search&JTS=true&JobType=8",
            "type": "html",
        },
        {
            "name": "remotive-software",
            "url": "https://remotive.com/api/remote-jobs?category=software-dev",
            "type": "api",
        },
    ]

    all_jobs = []
    source_stats = []

    for config in source_configs:
        try:
            if config["type"] == "html":
                result = _scrape_translatorscafe_listing(config["name"], config["url"])
                all_jobs.extend(result["jobs"])
                source_stats.append(
                    {
                        "source": result["source"],
                        "fetched": result["fetched"],
                        "valid": result["valid"],
                        "invalid": result["invalid"],
                        "error": None,
                    }
                )
            elif config["type"] == "api":
                jobs, stat = _scrape_remotive_api(config["name"], config["url"])
                all_jobs.extend(jobs)
                source_stats.append(stat)
        except Exception as exc:
            LOGGER.exception("Failed scraping source %s", config["name"])
            source_stats.append(
                {
                    "source": config["name"],
                    "fetched": 0,
                    "valid": 0,
                    "invalid": 0,
                    "error": str(exc),
                }
            )

    return all_jobs, source_stats


def _scrape_remotive_api(source_name, api_url):
    """Scrape jobs from Remotive public API for software jobs."""
    try:
        response = requests.get(
            api_url, timeout=REQUEST_TIMEOUT_SECONDS, headers=REQUEST_HEADERS)
        response.raise_for_status()
        data = response.json()
        jobs_raw = data.get("jobs", [])
    except Exception as exc:
        return [], {
            "source": source_name,
            "fetched": 0,
            "valid": 0,
            "invalid": 0,
            "error": str(exc),
        }

    jobs = []
    skipped_invalid = 0
    for job in jobs_raw:
        job_payload = {
            "title": _safe_text(job.get("title")),
            "company": _safe_text(job.get("company_name")),
            "location": _safe_text(job.get("candidate_required_location")),
            "description": _safe_text(job.get("description")),
            "url": _safe_text(job.get("url")),
            "posted_at": datetime.strptime(job.get("publication_date", ""), "%Y-%m-%dT%H:%M:%S%z") if job.get("publication_date") else datetime.utcnow(),
        }
        if not _is_valid_job_payload(job_payload):
            skipped_invalid += 1
            continue
        jobs.append(job_payload)

    return jobs, {
        "source": source_name,
        "fetched": len(jobs_raw),
        "valid": len(jobs),
        "invalid": skipped_invalid,
        "error": None,
    }


def scrape_example_jobs():
    """Backward-compatible alias now using the multi-source scraper."""
    jobs, _ = scrape_jobs_from_sources()
    return jobs


def _apply_updates_if_changed(existing_job, job_data):
    changed = False
    fields = ["title", "company", "location", "description", "url", "posted_at"]
    for field in fields:
        incoming = (
            _parse_datetime_or_now(job_data.get(field))
            if field == "posted_at"
            else job_data.get(field)
        )
        if getattr(existing_job, field) != incoming:
            setattr(existing_job, field, incoming)
            changed = True
    return changed


def store_jobs_in_db(jobs):
    """
    Upsert scraped jobs into the database.
    - Same URL: update existing job if details changed.
    - New URL: insert new job.
    """
    existing_jobs = Job.query.all()
    existing_by_url = {}
    existing_by_key = {}

    for job in existing_jobs:
        canonical_url = _canonicalize_job_url(job.url)
        if canonical_url:
            existing_by_url[canonical_url] = job

        fallback_key = _normalize_job_key(job.title, job.company, job.location, job.url)
        existing_by_key[fallback_key] = job

    inserted = 0
    updated = 0
    skipped = 0
    invalid = 0

    for job_data in jobs:
        if not _is_valid_job_payload(job_data):
            invalid += 1
            continue

        canonical_url = _canonicalize_job_url(job_data.get("url"))
        fallback_key = _normalize_job_key(
            job_data.get("title"),
            job_data.get("company"),
            job_data.get("location"),
            job_data.get("url"),
        )

        existing_job = existing_by_url.get(
            canonical_url) or existing_by_key.get(fallback_key)

        if existing_job:
            if _apply_updates_if_changed(existing_job, job_data):
                updated += 1
            else:
                skipped += 1
            continue

        new_job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            description=job_data["description"],
            url=canonical_url,
            posted_at=_parse_datetime_or_now(job_data.get("posted_at")),
        )
        db.session.add(new_job)
        inserted += 1

        if canonical_url:
            existing_by_url[canonical_url] = new_job
        existing_by_key[fallback_key] = new_job

    db.session.commit()

    return {
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "invalid": invalid,
    }
