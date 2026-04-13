import logging
import time
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from app.extension import db
from app.models import Job

LOGGER = logging.getLogger(__name__)

# Used for public JSON APIs that explicitly support programmatic access
API_HEADERS = {
    "User-Agent": "LangLocalJobsBot/1.0 (+https://github.com/EBUKA-EU/langlocaljobs)"}

# Used for HTML scraping — mimics a real browser to avoid blocks
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# Keep for backward compatibility
REQUEST_HEADERS = API_HEADERS
REQUEST_TIMEOUT_SECONDS = 20
HTML_REQUEST_DELAY_SECONDS = 2  # polite delay between HTML page requests


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
                            headers=BROWSER_HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# --- Source: Arbeitnow (https://www.arbeitnow.com) ---
# Free public job board API. Returns JSON with a "data" array.
# Endpoint: https://www.arbeitnow.com/api/job-board-api
def _scrape_arbeitnow_api(source_name, api_url):
    """Fetch jobs from the Arbeitnow public JSON API."""
    try:
        response = requests.get(
            api_url, timeout=REQUEST_TIMEOUT_SECONDS, headers=REQUEST_HEADERS)
        response.raise_for_status()
        data = response.json()
        jobs_raw = data.get("data", [])
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
        description = _safe_text(job.get("description")) or _safe_text(job.get("title"))
        job_payload = {
            "title": _safe_text(job.get("title")),
            "company": _safe_text(job.get("company_name")),
            "location": _safe_text(job.get("location")) or "Remote",
            "description": description,
            "url": _safe_text(job.get("url")),
            "posted_at": datetime.utcnow(),
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


# --- Source: The Muse (https://www.themuse.com) ---
# Free public jobs API. Returns JSON with a "results" array.
# Endpoint: https://www.themuse.com/api/public/jobs
def _scrape_themuse_api(source_name, api_url):
    """Fetch jobs from The Muse public JSON API."""
    try:
        response = requests.get(
            api_url, timeout=REQUEST_TIMEOUT_SECONDS, headers=REQUEST_HEADERS)
        response.raise_for_status()
        data = response.json()
        jobs_raw = data.get("results", [])
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
        company = job.get("company", {}).get("name", "")
        locations = job.get("locations", [])
        location = ", ".join(loc.get("name", "")
                             for loc in locations) if locations else "Remote"
        contents = _safe_text(job.get("contents")) or _safe_text(job.get("name"))
        job_url = _safe_text(job.get("refs", {}).get("landing_page"))
        job_payload = {
            "title": _safe_text(job.get("name")),
            "company": _safe_text(company),
            "location": location,
            "description": contents,
            "url": job_url,
            "posted_at": datetime.utcnow(),
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


# --- Source: RealPython Fake Jobs (https://realpython.github.io/fake-jobs/) ---
# A static GitHub Pages site with 100 fake job listings, designed for scraping practice.
# Each job is in a <div class="card"> with title (h2.title), company (h3.company),
# location (p.location), date (<time datetime="...">) and an "Apply" link.
def _scrape_realpython_fake_jobs(source_name, listing_url):
    """HTML-scrape job cards from the RealPython fake-jobs practice site."""
    try:
        time.sleep(HTML_REQUEST_DELAY_SECONDS)
        soup = _fetch_soup(listing_url)
    except Exception as exc:
        return [], {
            "source": source_name,
            "fetched": 0,
            "valid": 0,
            "invalid": 0,
            "error": str(exc),
        }

    cards = soup.find_all("div", class_="card")
    jobs = []
    skipped_invalid = 0

    for card in cards:
        title_tag = card.find("h2", class_="title")
        company_tag = card.find("h3", class_="company")
        location_tag = card.find("p", class_="location")
        time_tag = card.find("time")
        apply_link = None
        for a in card.find_all("a", href=True):
            if a.get_text(strip=True).lower() == "apply":
                apply_link = a["href"]
                break

        posted_at = datetime.utcnow()
        if time_tag and time_tag.get("datetime"):
            try:
                posted_at = datetime.strptime(time_tag["datetime"], "%Y-%m-%d")
            except ValueError:
                pass

        description = _safe_text(title_tag.get_text(
            " ", strip=True)) if title_tag else ""
        job_payload = {
            "title": _safe_text(title_tag.get_text(" ", strip=True)) if title_tag else "",
            "company": _safe_text(company_tag.get_text(" ", strip=True)) if company_tag else "",
            "location": _safe_text(location_tag.get_text(" ", strip=True)) if location_tag else "",
            "description": description or "Visit job link for full description.",
            "url": _canonicalize_job_url(apply_link or listing_url),
            "posted_at": posted_at,
        }

        if not _is_valid_job_payload(job_payload):
            skipped_invalid += 1
            continue
        jobs.append(job_payload)

    return jobs, {
        "source": source_name,
        "fetched": len(cards),
        "valid": len(jobs),
        "invalid": skipped_invalid,
        "error": None,
    }


def scrape_jobs_from_sources():
    """
    Scrape jobs from all configured sources.
    Each source is attempted independently — failures in one do not block others.
    Returns (all_jobs, source_stats) where source_stats has per-source metrics.
    """
    source_configs = [
        # realpython.github.io/fake-jobs — static GitHub Pages site with 100 fake listings
        {
            "name": "realpython-fake-jobs",
            "url": "https://realpython.github.io/fake-jobs/",
            "type": "realpython",
        },
        # remotive.com — remote jobs API, filtered to software-dev category
        {
            "name": "remotive-software",
            "url": "https://remotive.com/api/remote-jobs?category=software-dev",
            "type": "api",
        },
        # arbeitnow.com — free public job board API
        {
            "name": "arbeitnow",
            "url": "https://www.arbeitnow.com/api/job-board-api",
            "type": "arbeitnow",
        },
        # themuse.com — free public jobs API
        {
            "name": "themuse",
            "url": "https://www.themuse.com/api/public/jobs?page=1&per_page=100",
            "type": "themuse",
        },
    ]

    all_jobs = []
    source_stats = []

    for config in source_configs:
        try:
            if config["type"] == "realpython":
                jobs, stat = _scrape_realpython_fake_jobs(config["name"], config["url"])
                all_jobs.extend(jobs)
                source_stats.append(stat)
            elif config["type"] == "api":
                jobs, stat = _scrape_remotive_api(config["name"], config["url"])
                all_jobs.extend(jobs)
                source_stats.append(stat)
            elif config["type"] == "arbeitnow":
                jobs, stat = _scrape_arbeitnow_api(config["name"], config["url"])
                all_jobs.extend(jobs)
                source_stats.append(stat)
            elif config["type"] == "themuse":
                jobs, stat = _scrape_themuse_api(config["name"], config["url"])
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


# --- Source: Remotive (https://remotive.com) ---
# Free public API for remote job listings. Returns JSON with a "jobs" array.
# Endpoint: https://remotive.com/api/remote-jobs?category=<category>
def _scrape_remotive_api(source_name, api_url):
    """Fetch jobs from the Remotive public JSON API."""
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
        pub_date = job.get("publication_date")
        posted_at = datetime.utcnow()
        if pub_date:
            for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
                try:
                    posted_at = datetime.strptime(pub_date, fmt)
                    break
                except ValueError:
                    continue
        job_payload = {
            "title": _safe_text(job.get("title")),
            "company": _safe_text(job.get("company_name")),
            "location": _safe_text(job.get("candidate_required_location")),
            "description": _safe_text(job.get("description")),
            "url": _safe_text(job.get("url")),
            "posted_at": posted_at,
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
