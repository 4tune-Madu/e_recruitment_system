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
