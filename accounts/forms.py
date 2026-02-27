from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeekerProfile, Company


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('bio', 'skills', 'resume', 'location', 'linkedin_url', 'website')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g. French, Spanish, Localization, CAT tools'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'description', 'website', 'logo', 'location')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
