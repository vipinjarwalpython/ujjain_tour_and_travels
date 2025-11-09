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


# ==================== contact/models.py (ADD THIS MODEL) ====================


class Review(models.Model):
    """Model for customer reviews and ratings"""

    RATING_CHOICES = [
        (1, "⭐ - Poor"),
        (2, "⭐⭐ - Fair"),
        (3, "⭐⭐⭐ - Good"),
        (4, "⭐⭐⭐⭐ - Very Good"),
        (5, "⭐⭐⭐⭐⭐ - Excellent"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    DESTINATION_CHOICES = [
        ("kashmir", "Kashmir"),
        ("goa", "Goa"),
        ("kerala", "Kerala"),
        ("rajasthan", "Rajasthan"),
        ("himachal", "Himachal Pradesh"),
        ("uttarakhand", "Uttarakhand"),
        ("andaman", "Andaman & Nicobar"),
        ("northeast", "North East India"),
        ("ladakh", "Ladakh"),
        ("other", "Other"),
    ]

    # Customer Information
    customer_name = models.CharField(max_length=200, help_text="Customer's full name")
    customer_email = models.EmailField(
        validators=[EmailValidator()], help_text="Customer's email"
    )

    # Review Details
    destination = models.CharField(
        max_length=50, choices=DESTINATION_CHOICES, help_text="Travel destination"
    )
    package_name = models.CharField(
        max_length=300, blank=True, null=True, help_text="Package/Tour name"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES, help_text="Overall rating (1-5)"
    )
    title = models.CharField(max_length=200, help_text="Review title/headline")
    review_text = models.TextField(help_text="Detailed review")

    # Travel Details
    travel_date = models.DateField(help_text="When did they travel")

    # Ratings Breakdown
    service_rating = models.IntegerField(
        choices=RATING_CHOICES, default=5, help_text="Service quality"
    )
    value_rating = models.IntegerField(
        choices=RATING_CHOICES, default=5, help_text="Value for money"
    )
    accommodation_rating = models.IntegerField(
        choices=RATING_CHOICES, default=5, help_text="Accommodation quality"
    )

    # Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Review"
        verbose_name_plural = "Customer Reviews"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["destination"]),
        ]

    def __str__(self):
        return f"{self.customer_name} - {self.rating}⭐ - {self.destination}"

    def get_average_rating(self):
        """Calculate average of all rating categories"""
        return round(
            (
                self.rating
                + self.service_rating
                + self.value_rating
                + self.accommodation_rating
            )
            / 4,
            1,
        )

    def get_rating_stars(self):
        """Return star emoji string"""
        return "⭐" * self.rating
