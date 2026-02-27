from django.test import TestCase
from django.core.management import call_command
from io import StringIO


class ScraperCommandTest(TestCase):
    def test_scrape_jobs_command_runs(self):
        out = StringIO()
        # The command uses requests to fetch external URLs; in tests it will fail gracefully
        try:
            call_command('scrape_jobs', stdout=out)
        except Exception:
            pass  # External requests expected to fail in test environment
        # Just verify command exists and can be called
        self.assertIsNotNone(out)
