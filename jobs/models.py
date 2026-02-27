from django.db import models
from django.conf import settings


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    )
    CATEGORY_CHOICES = (
        ('translation', 'Translation'),
        ('interpretation', 'Interpretation'),
        ('localization', 'Localization'),
        ('transcription', 'Transcription'),
        ('subtitling', 'Subtitling'),
        ('copywriting', 'Copywriting'),
        ('proofreading', 'Proofreading'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='translation')
    skills_required = models.TextField(blank=True, help_text='Comma-separated skills')
    deadline = models.DateField(null=True, blank=True)
    source_url = models.URLField(blank=True, help_text='URL for scraped jobs')
    is_scraped = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='posted_jobs')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"


class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'user')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
