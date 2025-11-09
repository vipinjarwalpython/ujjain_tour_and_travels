from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry, Review


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "phone",
        "inquiry_type_badge",
        "status_badge",
        "created_at",
        "inquiry_age",
    ]
    list_filter = ["status", "inquiry_type", "created_at", "is_active"]
    search_fields = ["full_name", "email", "subject", "message", "phone"]
    readonly_fields = ["created_at", "updated_at", "inquiry_age"]
    list_per_page = 25
    date_hierarchy = "created_at"

    fieldsets = (
        ("Contact Information", {"fields": ("full_name", "email", "phone")}),
        ("Inquiry Details", {"fields": ("inquiry_type", "subject", "message")}),
        ("Status & Management", {"fields": ("status", "admin_notes", "is_active")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at", "inquiry_age"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["mark_as_in_progress", "mark_as_resolved", "mark_as_closed"]

    def inquiry_type_badge(self, obj):
        """Display inquiry type as colored badge"""
        colors = {
            "general": "#6c757d",
            "booking": "#007bff",
            "package": "#28a745",
            "complaint": "#dc3545",
            "feedback": "#ffc107",
        }
        color = colors.get(obj.inquiry_type, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_inquiry_type_display(),
        )

    inquiry_type_badge.short_description = "Type"

    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            "pending": "#ffc107",
            "in_progress": "#17a2b8",
            "resolved": "#28a745",
            "closed": "#6c757d",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def inquiry_age(self, obj):
        """Display inquiry age in days"""
        days = obj.get_inquiry_age_days()
        if days == 0:
            return format_html('<span style="color: green;">Today</span>')
        elif days == 1:
            return format_html('<span style="color: green;">Yesterday</span>')
        elif days <= 3:
            return format_html('<span style="color: orange;">{} days ago</span>', days)
        else:
            return format_html('<span style="color: red;">{} days ago</span>', days)

    inquiry_age.short_description = "Age"

    def mark_as_in_progress(self, request, queryset):
        """Bulk action to mark inquiries as in progress"""
        updated = queryset.update(status="in_progress")
        self.message_user(request, f"{updated} inquiries marked as in progress.")

    mark_as_in_progress.short_description = "Mark as In Progress"

    def mark_as_resolved(self, request, queryset):
        """Bulk action to mark inquiries as resolved"""
        updated = queryset.update(status="resolved")
        self.message_user(request, f"{updated} inquiries marked as resolved.")

    mark_as_resolved.short_description = "Mark as Resolved"

    def mark_as_closed(self, request, queryset):
        """Bulk action to mark inquiries as closed"""
        updated = queryset.update(status="closed")
        self.message_user(request, f"{updated} inquiries marked as closed.")

    mark_as_closed.short_description = "Mark as Closed"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer_name",
        "destination",
        "rating_stars",
        "status_badge",
        "is_featured",
        "travel_date",
        "created_at",
    ]
    list_filter = ["status", "rating", "destination", "is_featured", "created_at"]
    search_fields = ["customer_name", "customer_email", "title", "review_text"]
    readonly_fields = ["created_at", "updated_at", "average_rating_display"]
    list_per_page = 25
    date_hierarchy = "created_at"

    fieldsets = (
        ("Customer Information", {"fields": ("customer_name", "customer_email")}),
        (
            "Review Details",
            {
                "fields": (
                    "destination",
                    "package_name",
                    "title",
                    "review_text",
                    "travel_date",
                )
            },
        ),
        (
            "Ratings",
            {
                "fields": (
                    "rating",
                    "service_rating",
                    "value_rating",
                    "accommodation_rating",
                    "average_rating_display",
                )
            },
        ),
        (
            "Status & Management",
            {"fields": ("status", "is_featured", "admin_notes", "is_active")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    actions = ["approve_reviews", "reject_reviews", "feature_reviews"]

    def rating_stars(self, obj):
        """Display rating as stars"""
        return format_html(
            '<span style="color: #ffc107; font-size: 16px;">{}</span>',
            obj.get_rating_stars(),
        )

    rating_stars.short_description = "Rating"

    def status_badge(self, obj):
        """Display status as badge"""
        colors = {
            "pending": "#ffc107",
            "approved": "#28a745",
            "rejected": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def average_rating_display(self, obj):
        """Display average rating"""
        avg = obj.get_average_rating()
        return format_html(
            '<strong style="color: #667eea; font-size: 16px;">{} ⭐</strong>', avg
        )

    average_rating_display.short_description = "Average Rating"

    def approve_reviews(self, request, queryset):
        """Bulk approve reviews"""
        updated = queryset.update(status="approved")
        self.message_user(request, f"{updated} reviews approved successfully.")

    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        """Bulk reject reviews"""
        updated = queryset.update(status="rejected")
        self.message_user(request, f"{updated} reviews rejected.")

    reject_reviews.short_description = "Reject selected reviews"

    def feature_reviews(self, request, queryset):
        """Mark reviews as featured"""
        updated = queryset.filter(status="approved").update(is_featured=True)
        self.message_user(request, f"{updated} reviews marked as featured.")

    feature_reviews.short_description = "Mark as featured"
