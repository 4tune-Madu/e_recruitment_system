from django.urls import path
from . import views

app_name = "jobboard"

urlpatterns = [
    path("", views.home, name="home"),        # homepage
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path("jobs/", views.job_list, name="job_list"),
    path("<int:pk>/", views.job_detail, name="job_detail"),  
    #View for job creation
    path("jobs/create/", views.create_job, name="create_job"),
    # Update and delete job
    path("jobs/<int:job_id>/update/", views.update_job, name="update_job"),
    path("jobs/<int:job_id>/delete/", views.delete_job, name="delete_job"),
    # Job Apply
    path("apply/<int:job_id>/", views.apply_for_job, name="apply_for_job"),
]