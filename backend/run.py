# run.py
#
# This is the main entrypoint for your Flask application.
# It creates the app instance using the factory function and starts the development server.
#
# Usage: Run this file directly to start the backend server.


from app import create_app  # Import the app factory function
from app.services.scraping import scrape_jobs_from_sources, store_jobs_in_db
import click

app = create_app()  # Create the Flask app instance


@app.cli.command("scrape-jobs")
def scrape_jobs():
    """Scrape jobs and store them in the database."""
    jobs, source_stats = scrape_jobs_from_sources()
    result = store_jobs_in_db(jobs)

    for stat in source_stats:
        if stat["error"]:
            click.echo(
                f"Source {stat['source']}: FAILED ({stat['error']})"
            )
            continue
        click.echo(
            f"Source {stat['source']}: fetched={stat['fetched']}, "
            f"valid={stat['valid']}, invalid={stat['invalid']}"
        )

    click.echo(
        "Scraped "
        f"{len(jobs)} jobs. "
        f"Inserted {result['inserted']} new jobs, "
        f"updated {result['updated']} existing jobs, "
        f"skipped {result['skipped']} unchanged jobs, "
        f"invalid payloads {result['invalid']}."
    )


if __name__ == "__main__":
    # Only run the server if this script is executed directly (not imported)
    app.run(debug=True)  # Start the Flask development server with debug mode enabled
