from django.test import TestCase, Client
from django.urls import reverse
from .models import User, JobSeekerProfile, Company


class UserModelTest(TestCase):
    def setUp(self):
        self.jobseeker = User.objects.create_user(
            username='jobseeker1', password='pass123', user_type='jobseeker'
        )
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', user_type='recruiter'
        )

    def test_user_type(self):
        self.assertTrue(self.jobseeker.is_jobseeker())
        self.assertFalse(self.jobseeker.is_recruiter())
        self.assertTrue(self.recruiter.is_recruiter())
        self.assertFalse(self.recruiter.is_jobseeker())

    def test_jobseeker_profile_creation(self):
        profile = JobSeekerProfile.objects.create(user=self.jobseeker)
        self.assertEqual(str(profile), "jobseeker1's Profile")

    def test_company_creation(self):
        company = Company.objects.create(user=self.recruiter, name='Test Corp')
        self.assertEqual(str(company), 'Test Corp')


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'jobseeker',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_login_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
