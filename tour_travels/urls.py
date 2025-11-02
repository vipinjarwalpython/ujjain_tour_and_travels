from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/contact/", include("contact.urls")),
    path("api-auth/", include("rest_framework.urls")),  # Browsable API login
]
