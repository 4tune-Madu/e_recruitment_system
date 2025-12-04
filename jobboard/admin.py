from django.contrib import admin

# Register your models here.
from .models import JobListing

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'university', 'faculty', 'department', 'location', 'salary', 'date_posted')
    search_fields = ('job_title', 'university', 'faculty', 'department', 'location')
    list_filter = ('university', 'faculty', 'department', 'location', 'date_posted')
    ordering = ('-date_posted',)  # newest jobs first


from django.contrib import admin
from .models import JobListing, JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "job", "applied_at", "status")
    list_filter = ("status", "applied_at", "job")
    search_fields = ("name", "email", "job__job_title")
    readonly_fields = ("applied_at",)