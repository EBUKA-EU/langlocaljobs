from django import forms
from .models import Job, JobApplication


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'description', 'location', 'salary_min', 'salary_max',
                  'job_type', 'category', 'skills_required', 'deadline')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'e.g. French, Spanish, SDL Trados'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('cover_letter',)
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell us why you are a great fit...'}),
        }


class JobSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search jobs...'}))
    category = forms.ChoiceField(required=False, choices=[('', 'All Categories')] + list(Job.CATEGORY_CHOICES))
    job_type = forms.ChoiceField(required=False, choices=[('', 'All Types')] + list(Job.JOB_TYPE_CHOICES))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Location...'}))
