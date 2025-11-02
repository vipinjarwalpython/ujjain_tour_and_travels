from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone


class ContactInquiry(models.Model):
    """Model for storing customer contact inquiries"""

    INQUIRY_TYPES = [
        ("general", "General Inquiry"),
        ("booking", "Booking Related"),
        ("package", "Package Information"),
        ("complaint", "Complaint"),
        ("feedback", "Feedback"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )

    full_name = models.CharField(max_length=200, help_text="Customer's full name")
    email = models.EmailField(
        validators=[EmailValidator()], help_text="Customer's email address"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True,
        help_text="Customer's phone number",
    )
    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPES,
        default="general",
        help_text="Type of inquiry",
    )
    subject = models.CharField(max_length=300, help_text="Inquiry subject")
    message = models.TextField(help_text="Detailed message from customer")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Current status of inquiry",
    )
    admin_notes = models.TextField(
        blank=True, null=True, help_text="Internal notes for admin"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When inquiry was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When inquiry was last updated"
    )
    is_active = models.BooleanField(default=True, help_text="Is inquiry active?")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["email"]),
            models.Index(fields=["inquiry_type"]),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.subject} ({self.get_status_display()})"

    def get_inquiry_age_days(self):
        """Calculate how many days since inquiry was created"""
        return (timezone.now() - self.created_at).days
