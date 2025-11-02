from rest_framework import serializers
from .models import ContactInquiry
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
