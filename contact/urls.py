from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactInquiryViewSet

# Create router and register viewset
router = DefaultRouter()
router.register(r"inquiries", ContactInquiryViewSet, basename="contact-inquiry")

app_name = "contact"

urlpatterns = [
    path("", include(router.urls)),
]
