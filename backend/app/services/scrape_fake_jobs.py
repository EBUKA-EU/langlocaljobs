# scrape_fake_jobs.py
#
# Standalone script to scrape the RealPython GitHub fake jobs site and
# store the results in the database.
#
# Usage (from the backend/ directory, with the virtual environment active):
#   python app/services/scrape_fake_jobs.py

# fmt: off  # prevent import sorters from moving sys.path setup below app imports
import sys
import os
# Ensure the backend/ directory is on the path so the app package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app import create_app  # noqa: E402
from app.services.scraping import _scrape_realpython_fake_jobs, store_jobs_in_db  # noqa: E402
# fmt: on


SOURCE_NAME = "realpython-fake-jobs"
SOURCE_URL = "https://realpython.github.io/fake-jobs/"

app = create_app()

with app.app_context():
    print(f"Scraping {SOURCE_URL} ...")
    jobs, stat = _scrape_realpython_fake_jobs(SOURCE_NAME, SOURCE_URL)

    if stat["error"]:
        print(f"FAILED: {stat['error']}")
        sys.exit(1)

    print(
        f"Fetched {stat['fetched']} cards — "
        f"valid: {stat['valid']}, invalid: {stat['invalid']}"
    )

    result = store_jobs_in_db(jobs)
    print(
        f"Inserted {result['inserted']} new jobs, "
        f"updated {result['updated']} existing jobs, "
        f"skipped {result['skipped']} unchanged jobs, "
        f"invalid payloads {result['invalid']}."
    )
