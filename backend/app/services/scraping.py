# scraping.py
#
# Basic scraping prototype for job listings using requests and BeautifulSoup.

import requests
from bs4 import BeautifulSoup
from app.models import Job
from app.extension import db
from datetime import datetime


def scrape_example_jobs():
    """
    Scrapes example job data from a static HTML page (placeholder for real scraping).
    Returns a list of job dicts.
    """
    # Example: scrape jobs from a static HTML page (replace with real URL)
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []
    for job_elem in soup.find_all("div", class_="card-content"):
        title_elem = job_elem.find("h2", class_="title")
        company_elem = job_elem.find("h3", class_="company")
        location_elem = job_elem.find("p", class_="location")
        if None in (title_elem, company_elem, location_elem):
            continue
        jobs.append({
            "title": title_elem.text.strip(),
            "company": company_elem.text.strip(),
            "location": location_elem.text.strip(),
            "description": job_elem.text.strip(),
            "url": url,
            "posted_at": datetime.utcnow(),
        })
    return jobs


def store_jobs_in_db(jobs):
    """
    Stores a list of job dicts in the database.
    """
    for job_data in jobs:
        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            description=job_data["description"],
            url=job_data["url"],
            posted_at=job_data["posted_at"],
        )
        db.session.add(job)
    db.session.commit()
