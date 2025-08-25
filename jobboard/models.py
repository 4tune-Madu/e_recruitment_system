from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # Needed to reference your custom User model

class JobListing(models.Model):
    job_title = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    job_description = models.TextField()
    location = models.CharField(max_length=200, default="Ekiti State, Nigeria")
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # New field to track the admin who posted the job
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="posted_jobs"
    )

    def __str__(self):
        return self.job_title


#Model for job applications
#This is for the job application form
from django.conf import settings
from django.db import models

class JobApplication(models.Model):
    job = models.ForeignKey(
        'JobListing', 
        on_delete=models.CASCADE, 
        related_name='applications'
    )  # Link each application to a specific job listing

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,      # Optional for guest applicants
        blank=True,     # Optional in forms
        related_name='job_applications'
    )  # Link to registered user (optional)

    name = models.CharField(max_length=100)  # Applicant's name
    email = models.EmailField()              # Applicant's email
    cover_letter = models.TextField()        # Cover letter
    resume = models.FileField(upload_to='resumes/')  # Resume file
    applied_at = models.DateTimeField(auto_now_add=True)  # Date applied

    # Field to store generated PDF
    pdf_file = models.FileField(
        upload_to="applications_pdfs/", 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.job.job_title}"
