from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import ContactInquiry
from .serializers import (
    ContactInquirySerializer,
    ContactInquiryStatusUpdateSerializer,
    ContactInquiryStatsSerializer,
)
from .utils import send_contact_confirmation_email, send_admin_notification_email
import logging

logger = logging.getLogger("contact")


class ContactInquiryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Contact Inquiries with full CRUD operations

    Includes caching, email notifications, and custom actions

    Endpoints:
    - list: GET /api/contact/inquiries/
    - create: POST /api/contact/inquiries/
    - retrieve: GET /api/contact/inquiries/{id}/
    - update: PUT /api/contact/inquiries/{id}/
    - partial_update: PATCH /api/contact/inquiries/{id}/
    - destroy: DELETE /api/contact/inquiries/{id}/
    - update_status: POST /api/contact/inquiries/{id}/update_status/
    - statistics: GET /api/contact/inquiries/statistics/
    - recent: GET /api/contact/inquiries/recent/
    """

    queryset = ContactInquiry.objects.filter(is_active=True)
    serializer_class = ContactInquirySerializer

    def get_cache_key(self, identifier="list", **kwargs):
        """Generate unique cache key for different queries"""
        if identifier == "list":
            return "contact_inquiries_list"
        elif identifier == "detail":
            return f'contact_inquiry_{kwargs.get("pk")}'
        elif identifier == "stats":
            return "contact_inquiry_statistics"
        return f"contact_inquiry_{identifier}"

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        """
        List all active contact inquiries with caching
        Cached for 5 minutes to improve performance
        """
        logger.info("Fetching list of contact inquiries")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve single inquiry with caching
        Checks cache first before hitting database
        """
        pk = kwargs.get("pk")
        cache_key = self.get_cache_key("detail", pk=pk)

        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for inquiry #{pk}")
            return Response(cached_data)

        # If not in cache, get from database
        logger.info(f"❌ Cache miss for inquiry #{pk}, fetching from database")
        response = super().retrieve(request, *args, **kwargs)

        # Store in cache for 5 minutes
        cache.set(cache_key, response.data, 60 * 5)
        logger.info(f"Cached inquiry #{pk}")

        return response

    def create(self, request, *args, **kwargs):
        """
        Create new contact inquiry
        - Validates data
        - Saves to database
        - Sends confirmation email to customer (threaded)
        - Sends notification email to admin (threaded)
        - Clears cache
        """
        logger.info("Creating new contact inquiry")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the inquiry
        contact_inquiry = serializer.save()
        logger.info(f"Contact inquiry #{contact_inquiry.id} created successfully")

        # Send emails asynchronously using threading
        logger.info(
            f"Sending confirmation and notification emails for inquiry #{contact_inquiry.id}"
        )
        send_contact_confirmation_email(contact_inquiry)
        send_admin_notification_email(contact_inquiry)

        # Clear list cache
        cache.delete(self.get_cache_key("list"))
        cache.delete(self.get_cache_key("stats"))
        logger.info("Cleared list and statistics cache")

        return Response(
            {
                "status": "success",
                "message": "Your inquiry has been submitted successfully! You will receive a confirmation email shortly.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update contact inquiry (PUT)
        Clears relevant caches after update
        """
        pk = kwargs.get("pk")
        logger.info(f"Updating inquiry #{pk}")

        response = super().update(request, *args, **kwargs)

        # Clear caches
        cache.delete(self.get_cache_key("detail", pk=pk))
        cache.delete(self.get_cache_key("list"))
        cache.delete(self.get_cache_key("stats"))
        logger.info(f"Cleared cache for inquiry #{pk}")

        return response

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update contact inquiry (PATCH)
        Clears relevant caches after update
        """
        pk = kwargs.get("pk")
        logger.info(f"Partially updating inquiry #{pk}")

        response = super().partial_update(request, *args, **kwargs)

        # Clear caches
        cache.delete(self.get_cache_key("detail", pk=pk))
        cache.delete(self.get_cache_key("list"))
        cache.delete(self.get_cache_key("stats"))
        logger.info(f"Cleared cache for inquiry #{pk}")

        return response

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete inquiry (sets is_active=False)
        Preserves data for record keeping
        """
        pk = kwargs.get("pk")
        instance = self.get_object()

        logger.info(f"Soft deleting inquiry #{pk}")
        instance.is_active = False
        instance.save()

        # Clear caches
        cache.delete(self.get_cache_key("detail", pk=pk))
        cache.delete(self.get_cache_key("list"))
        cache.delete(self.get_cache_key("stats"))
        logger.info(f"Inquiry #{pk} soft deleted successfully")

        return Response(
            {"status": "success", "message": "Inquiry deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        """
        Custom action to update inquiry status
        POST /api/contact/inquiries/{id}/update-status/
        Body: {"status": "in_progress", "admin_notes": "Optional notes"}
        """
        inquiry = self.get_object()
        serializer = ContactInquiryStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            inquiry.status = serializer.validated_data["status"]
            if "admin_notes" in serializer.validated_data:
                inquiry.admin_notes = serializer.validated_data["admin_notes"]
            inquiry.save()

            # Clear caches
            cache.delete(self.get_cache_key("detail", pk=pk))
            cache.delete(self.get_cache_key("list"))
            cache.delete(self.get_cache_key("stats"))

            logger.info(f"Updated status for inquiry #{pk} to {inquiry.status}")

            response_serializer = self.get_serializer(inquiry)
            return Response(
                {
                    "status": "success",
                    "message": f"Status updated to {inquiry.get_status_display()}",
                    "data": response_serializer.data,
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def statistics(self, request):
        """
        Get inquiry statistics
        GET /api/contact/inquiries/statistics/
        Returns counts by status and type
        """
        logger.info("Fetching inquiry statistics")

        # Count by status
        total = ContactInquiry.objects.filter(is_active=True).count()
        pending = ContactInquiry.objects.filter(
            status="pending", is_active=True
        ).count()
        in_progress = ContactInquiry.objects.filter(
            status="in_progress", is_active=True
        ).count()
        resolved = ContactInquiry.objects.filter(
            status="resolved", is_active=True
        ).count()
        closed = ContactInquiry.objects.filter(status="closed", is_active=True).count()

        # Count by type
        by_type = {}
        for inquiry_type, display_name in ContactInquiry.INQUIRY_TYPES:
            count = ContactInquiry.objects.filter(
                inquiry_type=inquiry_type, is_active=True
            ).count()
            by_type[inquiry_type] = {"count": count, "display_name": display_name}

        # Recent inquiries (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_inquiries = ContactInquiry.objects.filter(
            created_at__gte=seven_days_ago, is_active=True
        ).count()

        stats = {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "resolved": resolved,
            "closed": closed,
            "by_type": by_type,
            "recent_inquiries": recent_inquiries,
        }

        logger.info(
            f"Statistics: Total={total}, Pending={pending}, Recent={recent_inquiries}"
        )

        return Response(stats)

    @action(detail=False, methods=["get"])
    @method_decorator(cache_page(60 * 2))  # Cache for 2 minutes
    def recent(self, request):
        """
        Get recent inquiries (last 10)
        GET /api/contact/inquiries/recent/
        """
        logger.info("Fetching recent inquiries")

        recent_inquiries = ContactInquiry.objects.filter(is_active=True).order_by(
            "-created_at"
        )[:10]

        serializer = self.get_serializer(recent_inquiries, many=True)
        return Response(
            {
                "status": "success",
                "count": len(serializer.data),
                "data": serializer.data,
            }
        )
