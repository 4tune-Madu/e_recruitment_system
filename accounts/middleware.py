from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedRedirectMiddleware:
    """
    Redirect users to the correct dashboard based on their role
    if they try to access the wrong dashboard.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip if user is not authenticated
        if request.user.is_authenticated:
            path = request.path

            # If normal user tries to access admin dashboard
            if not request.user.is_staff and path.startswith("/accounts/dashboard/admin/"):
                return redirect(reverse("accounts:user_dashboard"))

            # If admin tries to access user dashboard
            if request.user.is_staff and path.startswith("/accounts/dashboard/user/"):
                return redirect(reverse("admin_dashboard"))

        return self.get_response(request)
