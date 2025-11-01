# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')

    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_employer(self):
        return self.role == 'employer'

    def is_job_seeker(self):
        return self.role == 'job_seeker'

    def is_admin(self):
        return self.role == 'admin'

    def save(self, *args, **kwargs):
        # Ensure email is always lowercase
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def _str_(self):
        return self.email or self.username


# Apllication model for hired rejected nd pendding
"""
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


"""