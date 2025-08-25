from django.shortcuts import render, get_object_or_404, redirect
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobListing, JobApplication
from .forms import JobApplicationForm, JobForm

# Homepage
def home(request):
    return render(request, "jobboard/home.html")

# List all active jobs
def job_list(request):
    jobs = JobListing.objects.filter(is_active=True).order_by('-date_posted')
    return render(request, 'jobboard/job_list.html', {'jobs': jobs})

# Job details
def job_detail(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    return render(request, 'jobboard/job_detail.html', {'job': job})

# Dashboard view (redirect based on user role)
@login_required
def dashboard_view(request):
    context = {}  # you can add context data if needed
    if request.user.is_admin():
        return admin_dashboard(request)  # call admin dashboard
    else:
        return render(request, "jobboard/user_dashboard.html", context)

# Admin dashboard: post jobs and see existing ones
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobForm  # Make sure you have JobForm defined

@login_required
def admin_dashboard(request):
    # Only allow admin users
    if not request.user.is_admin():
        messages.error(request, "Access denied.")
        return redirect("jobboard:home")

    # Handle job posting form submission
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # Track which admin posted it
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("jobboard:admin_dashboard")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = JobForm()

    # Show jobs posted by this admin
    jobs = JobListing.objects.filter(posted_by=request.user).order_by('-date_posted')

    context = {
        "form": form,
        "jobs": jobs
    }
    return render(request, "jobboard/admin_dashboard.html", context)


# Apply for a job
from django.shortcuts import get_object_or_404, render, redirect
from .models import JobListing, JobApplication
from .forms import JobApplicationForm
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

def apply_for_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()

            # Generate PDF
            html_string = render_to_string('jobboard/application_pdf.html', {'application': application})
            pdf_file = HTML(string=html_string).write_pdf()

            # Save PDF to a file (optional)
            pdf_filename = f'application_{application.id}.pdf'
            with open(f'media/applications/{pdf_filename}', 'wb') as f:
                f.write(pdf_file)

            messages.success(request, "Application submitted successfully!")
            return redirect('jobboard:job_list')

    else:
        form = JobApplicationForm()

    return render(request, 'jobboard/apply_form.html', {'form': form, 'job': job})


# Job Create View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import JobForm

@login_required
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # assuming Job model has a posted_by field
            job.save()
            messages.success(request, "Job created successfully!")
            return redirect("accounts:admin_dashboard")  # back to admin dashboard
    else:
        form = JobForm()

    return render(request, "jobboard/create_job.html", {"form": form})



# Update and Delete views
from django.shortcuts import render, get_object_or_404, redirect
from .models import JobListing
from .forms import JobForm  # assuming your create form is called JobForm
from django.contrib import messages

def update_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("accounts:admin_dashboard")
    else:
        form = JobForm(instance=job)
    return render(request, "jobboard/create_job.html", {"form": form, "job": job})

def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("accounts:admin_dashboard")
    return render(request, "jobboard/job_confirm_delete.html", {"job": job})
