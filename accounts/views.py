from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm

# Sign Up View
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('accounts:login')  # namespaced
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


# Login View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import EmailAuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request.POST, request=request)  # pass request
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            # Redirect based on user role
            if user.role == 'admin':
                return redirect('accounts:admin_dashboard')
            else:  # For both employer and job seeker
                return redirect('accounts:user_dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm(request=request)  # pass request

    return render(request, 'accounts/login.html', {'form': form})

# User Dashboard
@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


# Admin Dashboard
from django.shortcuts import render
from jobboard.models import JobListing  # import JobListing model
from django.contrib.auth import get_user_model
from jobboard.models import JobListing, JobApplication


User = get_user_model()

def admin_dashboard(request):
    # Count all users
    total_users = User.objects.count()

    # Count roles
    total_admins = User.objects.filter(role='admin').count()
    total_jobseekers = User.objects.filter(role='job_seeker').count()
    total_employers = User.objects.filter(role='employer').count()  # if you add employers later

    # Fetch all jobs
    jobs = JobListing.objects.all().order_by('-date_posted')

    # Fetch all applications
    applications = JobApplication.objects.select_related('job').all().order_by('-applied_at')

    context = {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_jobseekers': total_jobseekers,
        'total_employers': total_employers,
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


# List Submitted applicants
from django.shortcuts import render, get_object_or_404
from jobboard.models import JobApplication

# List all applications for admin
def admin_applications(request):
    applications = JobApplication.objects.select_related('job', 'user').all().order_by('-applied_at')
    return render(request, 'accounts/admin_applications.html', {'applications': applications})

# Detail view for each application
def application_detail(request, id):
    application = get_object_or_404(JobApplication.objects.select_related('job', 'user'), id=id)
    return render(request, 'accounts/application_detail.html', {'application': application})


# View to fetch applications
from django.shortcuts import render
from jobboard.models import JobApplication

def admin_applications(request):
    # Fetch all job applications
    applications = JobApplication.objects.select_related('job').all().order_by('-applied_at')
    return render(request, 'accounts/admin_applications.html', {'applications': applications})


# View to show individual applications so it can be inspected in HTML
from django.shortcuts import render, get_object_or_404
from jobboard.models import JobListing, JobApplication

def application_detail(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)
    context = {
        'application': application,
    }
    return render(request, 'accounts/admin_application_detail.html', {'application':application})

# Logout view
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # redirect to login page after logout

# View to delete applicants applications
from django.shortcuts import render, get_object_or_404, redirect
from jobboard.models import JobApplication
from django.contrib import messages

def delete_application(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)

    if request.method == "POST":
        application.delete()
        messages.success(request, "Application deleted successfully.")
        return redirect('accounts:admin_dashboard')  # redirect after successful deletion

    # If GET request, show confirmation page
    return render(request, 'accounts/admin_application_confirm_delete.html', {'application': application})




# Hire / reject applicant
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from jobboard.models import JobApplication


@login_required
def hire_applicant(request, app_id):
    """Mark applicant as Hired and send congratulatory email."""
    application = get_object_or_404(JobApplication, id=app_id)
    application.status = "Hired"
    application.save()

    # Determine recipient email
    recipient_email = None
    if application.user and application.user.email:
        recipient_email = application.user.email
    elif application.email:
        recipient_email = application.email

    if recipient_email:
        subject = "🎉 Congratulations! You’ve been hired"
        html_message = render_to_string("emails/hire_email.html", {
            "user": application.user or application.name,
            "job": application.job,
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                html_message=html_message,
            )
            messages.success(request, f"{application.name} has been hired and notified via email.")
        except Exception as e:
            messages.warning(request, f"{application.name} was hired, but email failed to send. ({e})")
    else:
        messages.warning(request, f"{application.name} hired, but no email available.")

    return redirect("accounts:application_detail", app_id=app_id)


@login_required
def reject_applicant(request, app_id):
    """Mark applicant as Rejected and send polite rejection email."""
    application = get_object_or_404(JobApplication, id=app_id)
    application.status = "Rejected"
    application.save()

    # Determine recipient email
    recipient_email = None
    if application.user and application.user.email:
        recipient_email = application.user.email
    elif application.email:
        recipient_email = application.email

    if recipient_email:
        subject = "Application Update - Thank You for Applying"
        html_message = render_to_string("emails/reject_email.html", {
            "user": application.user or application.name,
            "job": application.job,
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                html_message=html_message,
            )
            messages.info(request, f"{application.name} has been rejected and notified via email.")
        except Exception as e:
            messages.warning(request, f"{application.name} rejected, but email failed to send. ({e})")
    else:
        messages.warning(request, f"{application.name} rejected, but no email available.")

    return redirect("accounts:application_detail", app_id=app_id)
