from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobListing, JobApplication
from .forms import  JobForm

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
import os
from io import BytesIO
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import formset_factory
from django.http import HttpResponse, FileResponse
from .models import JobListing, JobApplication
from .forms import Step1Form, ChildForm, EducationForm, QualificationForm, RefereeForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

import os
from io import BytesIO
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, FileResponse
from django.forms import formset_factory
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

from .models import (
    JobListing,
    JobApplication,
    ChildInfo,
    InstitutionAttended,
    Qualification,
    Referee
)
from .forms import Step1Form, ChildForm, EducationForm, QualificationForm, RefereeForm

def apply_for_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    # Session keys
    step_key = f"application_step_{job_id}"
    step1_key = f"step1_data_{job_id}"
    children_key = f"children_data_{job_id}"
    education_key = f"education_data_{job_id}"
    qualifications_key = f"qualifications_data_{job_id}"
    referees_key = f"referees_data_{job_id}"
    resumes_key = f"resumes_data_{job_id}"
    cover_letter_key = f"cover_letter_{job_id}"

    step = request.session.get(step_key, 1)

    # BACK button logic
    if request.GET.get("back"):
        if step > 1:
            request.session[step_key] = step - 1
        return redirect("jobboard:apply_for_job", job_id=job_id)

    # ---------------- STEP 1 ----------------
    if step == 1:
        saved_data = request.session.get(step1_key)
        if request.method == "POST":
            form = Step1Form(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data
                if cleaned.get("date_of_birth"):
                    cleaned["date_of_birth"] = cleaned["date_of_birth"].isoformat()
                request.session[step1_key] = cleaned
                request.session[step_key] = 2
                return redirect("jobboard:apply_for_job", job_id=job_id)
        else:
            form = Step1Form(initial=saved_data)
        return render(request, "jobboard/apply_step1.html", {"form": form, "job": job, "step": 1})

    # ---------------- STEP 2 ----------------
    if step == 2:
        saved_children = request.session.get(children_key, [])

        # Render one empty form only if NO saved children exist
        extra_forms = 1 if not saved_children else 0

        ChildFormSetClass = formset_factory(ChildForm, extra=extra_forms, can_delete=True)

        if request.method == "POST":
            formset = ChildFormSetClass(request.POST)

            if formset.is_valid():
                cleaned_children = []

                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                        cleaned_children.append({
                            "child_name": form.cleaned_data["child_name"],
                            "age": form.cleaned_data["age"],
                        })

                # Save to session
                request.session[children_key] = cleaned_children
                request.session[step_key] = 3
                return redirect("jobboard:apply_for_job", job_id=job_id)

        else:
            formset = ChildFormSetClass(initial=saved_children)

        # Add numbering for template display
        for idx, form in enumerate(formset.forms):
            form.child_number = idx + 1

        return render(request, "jobboard/apply_step2.html", {
            "job": job,
            "step": 2,
            "formset": formset
        })

    # ---------------- STEP 3 ----------------
    if step == 3:
        saved_education = request.session.get(education_key, [])

        # If no saved data, show 1 blank form
        extra_forms = 0 if saved_education else 1
        EducationFormSetClass = formset_factory(EducationForm, extra=extra_forms, can_delete=True)

        if request.method == "POST":
            formset = EducationFormSetClass(request.POST)
            if formset.is_valid():
                clean_education = []
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                        clean_education.append({
                            "school_name": form.cleaned_data["school_name"],
                            "degree": form.cleaned_data["degree"],
                            "field": form.cleaned_data["field"],
                            "graduation_year": form.cleaned_data["graduation_year"],
                        })
                request.session[education_key] = clean_education
                request.session[step_key] = 4
                return redirect("jobboard:apply_for_job", job_id=job_id)

        else:
            formset = EducationFormSetClass(initial=saved_education)

        for idx, form in enumerate(formset.forms):
            form.edu_number = idx + 1

        return render(request, "jobboard/apply_step3.html", {
            "job": job, "step": 3, "formset": formset
        })

    # ---------------- STEP 4 ----------------
    if step == 4:
        saved_qualifications = request.session.get(qualifications_key, [])
        QualificationFormSetClass = formset_factory(QualificationForm, extra=0, can_delete=True)
        if request.method == "POST":
            formset = QualificationFormSetClass(request.POST)
            if formset.is_valid():
                clean_qualifications = []
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                        clean_qualifications.append({
                            "institution_name": form.cleaned_data["institution_name"],
                            "degree": form.cleaned_data["degree"],
                            "field_of_study": form.cleaned_data["field_of_study"],
                            "graduation_year": form.cleaned_data["graduation_year"]
                        })
                request.session[qualifications_key] = clean_qualifications
                request.session[step_key] = 5
                return redirect("jobboard:apply_for_job", job_id=job_id)
        else:
            formset = QualificationFormSetClass(initial=saved_qualifications)
        for idx, form in enumerate(formset.forms):
            form.qual_number = idx + 1
        return render(request, "jobboard/apply_step4.html", {"job": job, "step": 4, "formset": formset})

    # ---------------- STEP 5 ----------------
    if step == 5:
        saved_referees = request.session.get(referees_key, [])
        RefereeFormSetClass = formset_factory(RefereeForm, extra=0, min_num=3, max_num=3, validate_min=True, validate_max=True, can_delete=False)
        if request.method == "POST":
            formset = RefereeFormSetClass(request.POST)
            if formset.is_valid():
                clean_refs = []
                for form in formset:
                    if form.cleaned_data:
                        clean_refs.append({"name": form.cleaned_data["name"], "address": form.cleaned_data["address"]})
                request.session[referees_key] = clean_refs
                request.session[step_key] = 6
                return redirect("jobboard:apply_for_job", job_id=job_id)
        else:
            formset = RefereeFormSetClass(initial=saved_referees)
        for idx, form in enumerate(formset.forms):
            form.ref_number = idx + 1
        return render(request, "jobboard/apply_step5.html", {"job": job, "step": 5, "formset": formset})

    # ---------------- STEP 6 ----------------
    if step == 6:
        existing_cover_letter = request.session.get(cover_letter_key, "")
        existing_files = request.session.get(resumes_key, [])

        if request.method == "POST":
            # Save cover letter
            cover_letter = request.POST.get("cover_letter", "")
            request.session[cover_letter_key] = cover_letter

            # Handle file deletion
            if "delete_file" in request.POST:
                index = int(request.POST["delete_file"])
                if 0 <= index < len(existing_files):
                    try:
                        os.remove(os.path.join(settings.MEDIA_ROOT, existing_files[index]))
                    except:
                        pass
                    existing_files.pop(index)
                    request.session[resumes_key] = existing_files
                return redirect("jobboard:apply_for_job", job_id=job_id)

            # Handle uploaded files
            uploaded = request.FILES.getlist("resumes")
            upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            for f in uploaded:
                file_path = f"uploads/{f.name}"
                full_path = os.path.join(upload_folder, f.name)
                with open(full_path, "wb+") as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
                existing_files.append(file_path)

            request.session[resumes_key] = existing_files
            request.session[step_key] = 7
            return redirect("jobboard:apply_for_job", job_id=job_id)

        return render(request, "jobboard/apply_step6.html", {
            "job": job,
            "step": 6,
            "existing_cover_letter": existing_cover_letter,
            "existing_files": existing_files,
            "MEDIA_URL": settings.MEDIA_URL,
        })

    # ---------------- STEP 7 ----------------
    if step == 7:
        step1_data = request.session.get(step1_key, {})
        children_data = request.session.get(children_key, [])
        education_data = request.session.get(education_key, [])
        qualifications_data = request.session.get(qualifications_key, [])
        referees_data = request.session.get(referees_key, [])
        resumes_files = request.session.get(resumes_key, [])
        cover_letter = request.session.get(cover_letter_key, "")
    
        # Build displayable resumes list for preview
        resumes_display = [{"name": os.path.basename(p), "url": settings.MEDIA_URL + p} for p in resumes_files]
    
        if request.method == "POST":
            # ----------------- SAVE TO DATABASE -----------------
            application = JobApplication.objects.create(
                job=job,
                user=request.user,
                name=step1_data.get("name", ""),
                email=step1_data.get("email", ""),
                date_of_birth=step1_data.get("date_of_birth"),
                place_of_birth=step1_data.get("place_of_birth", ""),
                home_address=step1_data.get("home_address", ""),
                postal_address=step1_data.get("postal_address", ""),
                telephone_number=step1_data.get("telephone_number", ""),
                nationality=step1_data.get("nationality", ""),
                state_of_origin=step1_data.get("state_of_origin", ""),
                marital_status=step1_data.get("marital_status", ""),
                cover_letter=cover_letter,
                resume=resumes_files[0] if resumes_files else None
            )
    
            # Save children info
            for child in children_data:
                ChildInfo.objects.create(
                    application=application,
                    child_name=child.get("child_name", ""),
                    age=child.get("age", 0)
                )
    
            # Save institutions attended
            for edu in education_data:
                InstitutionAttended.objects.create(
                    application=application,
                    name=edu.get("school_name", ""),
                    start_year=edu.get("start_year", 0),
                    end_year=edu.get("end_year", 0)
                )
    
            # Save qualifications
            for qual in qualifications_data:
                Qualification.objects.create(
                    application=application,
                    title=qual.get("degree", ""),
                    institution=qual.get("institution_name", ""),
                    year=qual.get("graduation_year", 0)
                )
    
            # Save referees
            for ref in referees_data:
                Referee.objects.create(
                    application=application,
                    name=ref.get("name", ""),
                    address=ref.get("address", ""),
                    phone=ref.get("phone", ""),
                    email=ref.get("email", "")
                )
    
            # ----------------- GENERATE PDF -----------------
            buffer = BytesIO()
            from reportlab.lib.pagesizes import LETTER
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
    
            width, height = LETTER
            y = height - inch
            p = canvas.Canvas(buffer, pagesize=LETTER)
    
            # Header
            p.setFont("Helvetica-Bold", 16)
            p.drawString(inch, y, "Job Application")
            y -= 0.5 * inch
    
            # Personal Info
            p.setFont("Helvetica-Bold", 12)
            p.drawString(inch, y, "Personal Information")
            y -= 0.25 * inch
            p.setFont("Helvetica", 11)
            for field, label in [
                ("name", "Name"), ("email", "Email"), ("date_of_birth", "Date of Birth"),
                ("place_of_birth", "Place of Birth"), ("home_address", "Home Address"),
                ("postal_address", "Postal Address"), ("telephone_number", "Phone"),
                ("nationality", "Nationality"), ("state_of_origin", "State of Origin"),
                ("marital_status", "Marital Status")
            ]:
                value = getattr(application, field, "")
                if value:
                    p.drawString(inch, y, f"{label}: {value}")
                    y -= 0.2 * inch
            y -= 0.1 * inch
    
            # Children
            children = application.children.all()
            if children:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(inch, y, "Children")
                y -= 0.25 * inch
                p.setFont("Helvetica", 11)
                for child in children:
                    p.drawString(inch, y, f"{child.child_name} — Age: {child.age}")
                    y -= 0.2 * inch
                y -= 0.1 * inch
    
            # Institutions
            institutions = application.institutions.all()
            if institutions:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(inch, y, "Institutions Attended")
                y -= 0.25 * inch
                p.setFont("Helvetica", 11)
                for inst in institutions:
                    p.drawString(inch, y, f"{inst.name} ({inst.start_year} - {inst.end_year})")
                    y -= 0.2 * inch
                y -= 0.1 * inch
    
            # Qualifications
            qualifications = application.qualifications.all()
            if qualifications:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(inch, y, "Qualifications")
                y -= 0.25 * inch
                p.setFont("Helvetica", 11)
                for qual in qualifications:
                    p.drawString(inch, y, f"{qual.title} — {qual.institution} ({qual.year})")
                    y -= 0.2 * inch
                y -= 0.1 * inch
    
            # Referees
            referees = application.referees.all()
            if referees:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(inch, y, "Referees")
                y -= 0.25 * inch
                p.setFont("Helvetica", 11)
                for ref in referees:
                    p.drawString(inch, y, f"{ref.name} — {ref.address} — {ref.phone} — {ref.email}")
                    y -= 0.2 * inch
                y -= 0.1 * inch
    
            # Cover Letter
            if application.cover_letter:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(inch, y, "Cover Letter")
                y -= 0.25 * inch
                p.setFont("Helvetica", 11)
                for line in application.cover_letter.splitlines():
                    if y < inch:
                        p.showPage()
                        y = height - inch
                    p.drawString(inch, y, line)
                    y -= 0.18 * inch
    
            # Resumes
            if resumes_files:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(inch, y, "Resumes")
                y -= 0.25 * inch
                p.setFont("Helvetica", 11)
                for resume_path in resumes_files:
                    if y < inch:
                        p.showPage()
                        y = height - inch
                    p.drawString(inch, y, os.path.basename(resume_path))
                    y -= 0.18 * inch
    
            p.showPage()
            p.save()
            buffer.seek(0)
    
            # ----------------- CLEAR SESSION -----------------
            for key in [step_key, step1_key, children_key, education_key, qualifications_key, referees_key, resumes_key, cover_letter_key]:
                request.session.pop(key, None)
    
            return FileResponse(buffer, as_attachment=True, filename="job_application.pdf")
    
        # ----------------- RENDER PREVIEW -----------------
        return render(request, "jobboard/apply_step7.html", {
            "job": job,
            "step": 7,
            "step1_data": step1_data,
            "children_data": children_data,
            "education_data": education_data,
            "qualifications_data": qualifications_data,
            "referees_data": referees_data,
            "resumes_files": resumes_display,
            "cover_letter": cover_letter,
        })
    
    return HttpResponse("Unknown step")
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

