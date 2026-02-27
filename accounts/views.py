from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, JobSeekerProfileForm, CompanyForm
from .models import JobSeekerProfile, Company


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'jobseeker':
                JobSeekerProfile.objects.create(user=user)
            else:
                Company.objects.create(user=user, name=f"{user.username}'s Company")
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', '/'))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/')


@login_required
def profile(request):
    if request.user.user_type == 'recruiter':
        return redirect('accounts:recruiter_profile')
    try:
        profile_obj = request.user.jobseeker_profile
    except JobSeekerProfile.DoesNotExist:
        profile_obj = JobSeekerProfile.objects.create(user=request.user)
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = JobSeekerProfileForm(instance=profile_obj)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile_obj})


@login_required
def recruiter_profile(request):
    if request.user.user_type != 'recruiter':
        return redirect('accounts:profile')
    try:
        company = request.user.company
    except Company.DoesNotExist:
        company = Company.objects.create(user=request.user, name=f"{request.user.username}'s Company")
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated!')
            return redirect('accounts:recruiter_profile')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'accounts/recruiter_profile.html', {'form': form, 'company': company})
