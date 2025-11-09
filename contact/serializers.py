from rest_framework import serializers
from .models import ContactInquiry, Review
from django.utils import timezone


class ContactInquirySerializer(serializers.ModelSerializer):
    """Serializer for ContactInquiry model with additional fields"""

    inquiry_type_display = serializers.CharField(
        source="get_inquiry_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    inquiry_age_days = serializers.SerializerMethodField()

    class Meta:
        model = ContactInquiry
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "inquiry_type",
            "inquiry_type_display",
            "subject",
            "message",
            "status",
            "status_display",
            "admin_notes",
            "created_at",
            "updated_at",
            "is_active",
            "inquiry_age_days",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "inquiry_age_days"]
        extra_kwargs = {"admin_notes": {"write_only": True}}

    def get_inquiry_age_days(self, obj):
        """Get number of days since inquiry was created"""
        return obj.get_inquiry_age_days()

    def validate_email(self, value):
        """Normalize email to lowercase"""
        return value.lower().strip()

    def validate_phone(self, value):
        """Validate and clean phone number"""
        if value:
            value = (
                value.replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )
        return value

    def validate_full_name(self, value):
        """Validate full name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()

    def validate_subject(self, value):
        """Validate subject"""
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Subject must be at least 5 characters long"
            )
        return value.strip()

    def validate_message(self, value):
        """Validate message"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long"
            )
        return value.strip()


class ContactInquiryStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating inquiry status"""

    status = serializers.ChoiceField(choices=ContactInquiry.STATUS_CHOICES)
    admin_notes = serializers.CharField(required=False, allow_blank=True)


class ContactInquiryStatsSerializer(serializers.Serializer):
    """Serializer for inquiry statistics"""

    total = serializers.IntegerField()
    pending = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    resolved = serializers.IntegerField()
    closed = serializers.IntegerField()
    by_type = serializers.DictField()
    recent_inquiries = serializers.IntegerField()


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""

    rating_display = serializers.CharField(source="get_rating_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    destination_display = serializers.CharField(
        source="get_destination_display", read_only=True
    )
    rating_stars = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "destination",
            "destination_display",
            "package_name",
            "rating",
            "rating_display",
            "rating_stars",
            "title",
            "review_text",
            "travel_date",
            "service_rating",
            "value_rating",
            "accommodation_rating",
            "average_rating",
            "status",
            "status_display",
            "is_featured",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "average_rating"]
        extra_kwargs = {"admin_notes": {"write_only": True}}

    def get_rating_stars(self, obj):
        """Get star emoji representation"""
        return obj.get_rating_stars()

    def get_average_rating(self, obj):
        """Get average rating"""
        return obj.get_average_rating()

    def validate_rating(self, value):
        """Validate rating is between 1-5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate_customer_email(self, value):
        """Normalize email"""
        return value.lower().strip()

    def validate_travel_date(self, value):
        """Validate travel date is not in future"""
        from django.utils import timezone

        if value > timezone.now().date():
            raise serializers.ValidationError("Travel date cannot be in the future")
        return value


class ReviewStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating review status"""

    status = serializers.ChoiceField(choices=Review.STATUS_CHOICES)
    admin_notes = serializers.CharField(required=False, allow_blank=True)
    is_featured = serializers.BooleanField(required=False)


class ReviewStatsSerializer(serializers.Serializer):
    """Serializer for review statistics"""

    total_reviews = serializers.IntegerField()
    approved_reviews = serializers.IntegerField()
    pending_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
    featured_reviews = serializers.IntegerField()
    by_destination = serializers.DictField()
    by_rating = serializers.DictField()
