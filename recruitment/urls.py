from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),

    # Homepage comes from jobboard (with namespace)
    path("", include(("jobboard.urls", "jobboard"), namespace="jobboard")),

    # Accounts (login/signup) with namespace
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]

# FOR MEDIA
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

