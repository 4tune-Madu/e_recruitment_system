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
    return render(request, 'accounts/admin_application_detail.html', context)

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

