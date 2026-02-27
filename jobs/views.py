from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, JobApplication, SavedJob
from .forms import JobForm, JobApplicationForm, JobSearchForm


def home(request):
    featured_jobs = Job.objects.filter(is_active=True).select_related('company')[:6]
    recent_jobs = Job.objects.filter(is_active=True).select_related('company').order_by('-created_at')[:10]
    categories = Job.CATEGORY_CHOICES
    return render(request, 'jobs/home.html', {
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'categories': categories,
    })


def job_list(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.filter(is_active=True).select_related('company')
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        job_type = form.cleaned_data.get('job_type')
        location = form.cleaned_data.get('location')
        if q:
            jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills_required__icontains=q))
        if category:
            jobs = jobs.filter(category=category)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if location:
            jobs = jobs.filter(location__icontains=location)
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'form': form})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    is_saved = False
    has_applied = False
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(job=job, user=request.user).exists()
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'is_saved': is_saved,
        'has_applied': has_applied,
    })


@login_required
def post_job(request):
    if not request.user.is_recruiter():
        messages.error(request, 'Only recruiters can post jobs.')
        return redirect('jobs:home')
    try:
        company = request.user.company
    except Exception:
        messages.error(request, 'Please set up your company profile first.')
        return redirect('accounts:recruiter_profile')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Post'})


@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Edit', 'job': job})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    if job.is_scraped and job.source_url:
        return redirect(job.source_url)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('jobs:job_detail', pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobs:job_detail', pk=pk)
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply_form.html', {'form': form, 'job': job})


@login_required
def save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    saved, created = SavedJob.objects.get_or_create(job=job, user=request.user)
    if not created:
        saved.delete()
        messages.info(request, 'Job removed from saved jobs.')
    else:
        messages.success(request, 'Job saved!')
    return redirect('jobs:job_detail', pk=pk)


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company')
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved})


@login_required
def recruiter_dashboard(request):
    if not request.user.is_recruiter():
        return redirect('jobs:home')
    jobs = Job.objects.filter(posted_by=request.user).prefetch_related('applications')
    return render(request, 'jobs/dashboard.html', {'jobs': jobs})


@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        job.is_active = False
        job.save()
        messages.success(request, 'Job deactivated.')
    return redirect('jobs:dashboard')
