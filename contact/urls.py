from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactInquiryViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"inquiries", ContactInquiryViewSet, basename="contact-inquiry")
router.register(r"reviews", ReviewViewSet, basename="review")

app_name = "contact"

urlpatterns = [
    path("", include(router.urls)),
]
