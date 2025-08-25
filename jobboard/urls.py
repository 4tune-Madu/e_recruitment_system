from django.urls import path
from . import views

app_name = "jobboard"

urlpatterns = [
    path("", views.home, name="home"),        # homepage
    path("jobs/", views.job_list, name="job_list"),
    path("<int:pk>/", views.job_detail, name="job_detail"),
    path("<int:job_id>/apply/", views.apply_for_job, name="apply_for_job"),  
    #View for job creation
    path("jobs/create/", views.create_job, name="create_job"),
    # Update and delete job
    path("jobs/<int:job_id>/update/", views.update_job, name="update_job"),
    path("jobs/<int:job_id>/delete/", views.delete_job, name="delete_job"),
]
