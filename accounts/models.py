from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)  # Ensure unique emails
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # username still required for superuser creation

    def is_employer(self):
        return self.role == 'employer'

    def is_job_seeker(self):
        return self.role == 'job_seeker'

    def is_admin(self):
        return self.role == 'admin'

    def save(self, *args, **kwargs):
        # Save email in lowercase for case-insensitive login
        self.email = self.email.lower()
        super().save(*args, **kwargs)




# Apllication model for hired rejected nd pendding
from django.conf import settings
from django.db import models

class JobApplication(models.Model):
    job = models.ForeignKey("jobboard.JobListing", on_delete=models.CASCADE)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Hired", "Hired"), ("Rejected", "Rejected")],
        default="Pending",
    )

    def __str__(self):
        return f"{self.user} - {self.job}"


