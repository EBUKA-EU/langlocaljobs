from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (('jobseeker', 'Job Seeker'), ('recruiter', 'Recruiter'))
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='jobseeker')

    def is_recruiter(self):
        return self.user_type == 'recruiter'

    def is_jobseeker(self):
        return self.user_type == 'jobseeker'


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
