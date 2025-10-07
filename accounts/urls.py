from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Admin Dashboard
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    
    # Admin: view all job applications
    path("dashboard/admin/applications/", views.admin_applications, name="admin_applications"),
    
    # Admin: view a single application detail
    path("dashboard/admin/applications/<int:app_id>/", views.application_detail, name="application_detail"),
    
    # User Dashboard
    path("dashboard/user/", views.user_dashboard, name="user_dashboard"),
    
    # User: view submitted applications
    path("dashboard/user/applications/", views.admin_applications, name="admin_applications"),

    # Admin: view a single application detail
    path(
    "dashboard/admin/applications/<int:app_id>/", views.application_detail, name="application_detail"),
    
    # Authentication , signup and logout URLs
    path("login/", views.login_view, name="login"),      
    path("signup/", views.signup_view, name="signup"), 
    path("logout/", views.logout_view, name="logout"), 

    # URL for deleting applications
    path(
    "dashboard/admin/applications/<int:app_id>/delete/", views.delete_application, name="delete_application"),

    # URL for hire/ reject
path("applications/<int:app_id>/hire/", views.hire_applicant, name="hire_applicant"),
path("applications/<int:app_id>/reject/", views.reject_applicant, name="reject_applicant"),    
]
