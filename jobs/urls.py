from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/saved/', views.saved_jobs, name='saved_jobs'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:pk>/save/', views.save_job, name='save_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('dashboard/', views.recruiter_dashboard, name='dashboard'),
]
