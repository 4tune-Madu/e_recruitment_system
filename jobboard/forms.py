from django import forms
# from .models import Job, JobApplication
from .models import JobListing, JobApplication



# Form for admin to post jobs
class JobForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['job_title', 'job_description', 'location', 'is_active', 'university', 'faculty', 'department', 'salary']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

#+++++++++++++++++++++++++++++++++++++
# Begining of form for Job Apllication
#+++++++++++++++++++++++++++++++++++++

from django import forms

class Step1Form(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Full name"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"you@example.com"})
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type":"date", "class":"form-control"})
    )
    place_of_birth = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"City, Country"})
    )
    home_address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class":"form-control", "rows":"2", "placeholder":"Home address"})
    )
    postal_address = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Postal address"})
    )
    telephone_number = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"+234 801 234 5678"})
    )
    nationality = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Nationality"})
    )
    state_of_origin = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"State of origin"})
    )
    MARITAL_CHOICES = [
        ("Single","Single"),
        ("Married","Married"),
        ("Divorced","Divorced"),
        ("Widowed","Widowed"),
    ]
    marital_status = forms.ChoiceField(
        choices=MARITAL_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class":"form-select"})
    )

    
class ChildForm(forms.Form):
    child_name = forms.CharField(max_length=200)
    age = forms.IntegerField()

class InstitutionForm(forms.Form):
    name = forms.CharField(max_length=255)
    start_year = forms.IntegerField()
    end_year = forms.IntegerField()

class QualificationForm(forms.Form):
    title = forms.CharField(max_length=255)
    institution = forms.CharField(max_length=255)
    year = forms.IntegerField()

class Step4Form(forms.Form):
    cover_letter = forms.CharField(widget=forms.Textarea)
    resume = forms.FileField()

class RefereeForm(forms.Form):
    name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()


#++++++++++++++++++++++++++++++++
# End of form for Job Apllication
#++++++++++++++++++++++++++++++++


from django import forms
from django.forms import formset_factory

class ChildForm(forms.Form):
    child_name = forms.CharField(
        max_length=100,
        label="Child's Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Child's Name"})
    )
    age = forms.IntegerField(
        min_value=0,
        label="Age",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Age"})
    )

ChildFormSet = formset_factory(ChildForm, extra=0, can_delete=True)  # extra=0, we'll handle dynamically


#Education Form
from django import forms

class EducationForm(forms.Form):
    school_name = forms.CharField(
        max_length=255,
        label="School Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "School Name"}),
    )
    degree = forms.CharField(
        max_length=255,
        label="Degree",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Degree"}),
    )
    field = forms.CharField(
        max_length=255,
        label="Field of Study",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Field of Study"}),
    )
    graduation_year = forms.IntegerField(
        label="Graduation Year",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "YYYY"}),
    )

#Qualificayioons
from django import forms

class QualificationForm(forms.Form):
    institution_name = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': "Institution Name", 'class': 'form-control'})
    )
    degree = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': "Degree", 'class': 'form-control'})
    )
    field_of_study = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': "Field of Study", 'class': 'form-control'})
    )
    graduation_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': "Graduation Year", 'class': 'form-control'})
    )

# Referee form
from django import forms

class RefereeForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': "Referee's Name",
            'class': 'form-control'
        })
    )
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': "Referee's Address",
            'class': 'form-control'
        })
    )