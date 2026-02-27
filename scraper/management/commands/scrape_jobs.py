import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from jobs.models import Job


SCRAPE_SOURCES = [
    {
        'name': 'ProZ.com Jobs (Example)',
        'url': 'https://www.proz.com/job-search',
        'parser': 'proz',
    },
]


def parse_proz(soup, source_url):
    """
    Example parser for ProZ.com style job listings.
    This is a demonstration parser - actual site structure may differ.
    Returns a list of job dicts.
    """
    jobs = []
    # Look for job listing elements - adjust selectors to match real site
    job_items = soup.find_all('div', class_='job-item') or soup.find_all('tr', class_='job')
    for item in job_items:
        title_el = item.find(['h2', 'h3', 'a', 'td'], class_=['job-title', 'title'])
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        link = title_el.find('a')
        job_url = link['href'] if link and link.get('href') else source_url
        if job_url and not job_url.startswith('http'):
            job_url = 'https://www.proz.com' + job_url
        desc_el = item.find(['p', 'div'], class_=['description', 'job-desc'])
        description = desc_el.get_text(strip=True) if desc_el else title
        location_el = item.find(['span', 'td'], class_=['location', 'job-location'])
        location = location_el.get_text(strip=True) if location_el else 'Remote'
        jobs.append({
            'title': title[:200],
            'description': description or title,
            'location': location[:200],
            'source_url': job_url,
            'category': 'translation',
            'job_type': 'freelance',
        })
    return jobs


PARSERS = {
    'proz': parse_proz,
}


class Command(BaseCommand):
    help = 'Scrape job listings from external sources and save to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print scraped jobs without saving to database',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        total_new = 0

        for source in SCRAPE_SOURCES:
            self.stdout.write(f"Scraping: {source['name']} ({source['url']})")
            try:
                headers = {
                    'User-Agent': (
                        'Mozilla/5.0 (compatible; LangLocalJobs/1.0; '
                        '+https://github.com/langlocaljobs)'
                    )
                }
                response = requests.get(source['url'], headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                parser_fn = PARSERS.get(source['parser'])
                if not parser_fn:
                    self.stdout.write(self.style.WARNING(f"  No parser found for {source['parser']}"))
                    continue
                jobs_data = parser_fn(soup, source['url'])
                self.stdout.write(f"  Found {len(jobs_data)} job(s)")
                for job_data in jobs_data:
                    if dry_run:
                        self.stdout.write(f"  [DRY RUN] Would save: {job_data['title']}")
                        continue
                    _, created = Job.objects.get_or_create(
                        source_url=job_data['source_url'],
                        defaults={
                            'title': job_data['title'],
                            'description': job_data['description'],
                            'location': job_data['location'],
                            'category': job_data.get('category', 'translation'),
                            'job_type': job_data.get('job_type', 'freelance'),
                            'is_scraped': True,
                            'is_active': True,
                        }
                    )
                    if created:
                        total_new += 1
                        self.stdout.write(self.style.SUCCESS(f"  Saved: {job_data['title']}"))
                    else:
                        self.stdout.write(f"  Already exists: {job_data['title']}")
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Error fetching {source['url']}: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Unexpected error for {source['name']}: {e}"))

        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f"\nDone! Saved {total_new} new job(s)."))
        else:
            self.stdout.write(self.style.SUCCESS(f"\nDry run complete."))
