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
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        'JobListing',
        on_delete=models.CASCADE,
        related_name='applications'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='job_applications'
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    # New status field with choices & default
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    pdf_file = models.FileField(upload_to="applications_pdfs/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.job.job_title}"
