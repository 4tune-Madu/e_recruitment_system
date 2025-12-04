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
# jobboard/models.py

#---------------------------------------------------
# This is the beginning of the job appliation models
#---------------------------------------------------

from django.conf import settings
from django.db import models


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey('JobListing', on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    # Step 1 fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    home_address = models.TextField(blank=True)
    postal_address = models.CharField(max_length=200, blank=True)
    telephone_number = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    state_of_origin = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)

    # Step 4 fields
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')

    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    pdf_file = models.FileField(upload_to="applications_pdfs/", null=True, blank=True)

    def _str_(self):
        return f"{self.name} - {self.job.job_title}"


class ChildInfo(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='children')
    child_name = models.CharField(max_length=200)
    age = models.IntegerField()

class InstitutionAttended(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='institutions')
    name = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

class Qualification(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='qualifications')
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.IntegerField()

class Referee(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='referees')
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()


#---------------------------------------------
# This is the end of the job appliation models
#---------------------------------------------