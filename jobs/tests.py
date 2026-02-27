from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Company
from .models import Job, JobApplication, SavedJob


class JobModelTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', user_type='recruiter'
        )
        self.company = Company.objects.create(user=self.recruiter, name='Test Corp')
        self.job = Job.objects.create(
            title='French Translator',
            description='We need a French translator',
            company=self.company,
            location='Remote',
            job_type='full-time',
            category='translation',
            posted_by=self.recruiter,
        )

    def test_job_str(self):
        self.assertEqual(str(self.job), 'French Translator')

    def test_job_is_active_by_default(self):
        self.assertTrue(self.job.is_active)

    def test_job_application_str(self):
        jobseeker = User.objects.create_user(username='js1', password='pass123', user_type='jobseeker')
        app = JobApplication.objects.create(job=self.job, applicant=jobseeker)
        self.assertEqual(str(app), 'js1 - French Translator')

    def test_saved_job_str(self):
        jobseeker = User.objects.create_user(username='js2', password='pass123', user_type='jobseeker')
        saved = SavedJob.objects.create(job=self.job, user=jobseeker)
        self.assertEqual(str(saved), 'js2 saved French Translator')


class JobViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.recruiter = User.objects.create_user(
            username='recruiter2', password='pass123', user_type='recruiter'
        )
        self.company = Company.objects.create(user=self.recruiter, name='Corp2')
        self.job = Job.objects.create(
            title='Spanish Interpreter',
            description='Need interpreter',
            company=self.company,
            location='New York',
            job_type='contract',
            category='interpretation',
            posted_by=self.recruiter,
        )

    def test_home_view(self):
        response = self.client.get(reverse('jobs:home'))
        self.assertEqual(response.status_code, 200)

    def test_job_list_view(self):
        response = self.client.get(reverse('jobs:job_list'))
        self.assertEqual(response.status_code, 200)

    def test_job_detail_view(self):
        response = self.client.get(reverse('jobs:job_detail', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)

    def test_job_list_search(self):
        response = self.client.get(reverse('jobs:job_list') + '?q=Spanish')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spanish Interpreter')
