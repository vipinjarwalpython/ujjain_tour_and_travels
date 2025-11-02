import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger("contact")


class EmailThread(threading.Thread):
    """
    Custom thread class for sending emails asynchronously
    This ensures email sending doesn't block the API response
    """

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
        self.daemon = True  # Thread will close when main program exits

    def run(self):
        """Execute email sending in separate thread"""
        try:
            self.email_message.send(fail_silently=False)
            logger.info(f"Email sent successfully to {self.email_message.to}")
        except Exception as e:
            logger.error(
                f"Failed to send email to {self.email_message.to}: {str(e)}"
            )


def send_contact_confirmation_email(contact_inquiry):
    """
    Send confirmation email to customer
    Uses threading for non-blocking operation
    """
    try:
        subject = f"Thank You for Contacting Tour & Travels - {contact_inquiry.subject}"

        context = {
            "name": contact_inquiry.full_name,
            "inquiry_type": contact_inquiry.get_inquiry_type_display(),
            "subject": contact_inquiry.subject,
            "message": contact_inquiry.message,
            "inquiry_id": contact_inquiry.id,
            "year": 2025,
        }

        # Render HTML email template
        html_content = render_to_string("emails/contact_confirmation.html", context)
        text_content = strip_tags(html_content)

        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact_inquiry.email],
        )
        email.attach_alternative(html_content, "text/html")

        # Send email in separate thread
        EmailThread(email).start()

        logger.info(f"Confirmation email queued for {contact_inquiry.email}")
        return True

    except Exception as e:
        logger.error(f"Error preparing confirmation email: {str(e)}")
        return False


def send_admin_notification_email(contact_inquiry):
    """
    Send notification email to admin
    Uses threading for non-blocking operation
    """
    try:
        subject = f"New Inquiry: {contact_inquiry.inquiry_type.upper()} - {contact_inquiry.subject}"

        context = {
            "inquiry": contact_inquiry,
            "inquiry_id": contact_inquiry.id,
            "name": contact_inquiry.full_name,
            "email": contact_inquiry.email,
            "phone": contact_inquiry.phone or "Not provided",
            "inquiry_type": contact_inquiry.get_inquiry_type_display(),
            "subject": contact_inquiry.subject,
            "message": contact_inquiry.message,
            "created_at": contact_inquiry.created_at,
            "year": 2025,
        }

        # Render HTML email template
        html_content = render_to_string("emails/admin_notification.html", context)
        text_content = strip_tags(html_content)

        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.attach_alternative(html_content, "text/html")

        # Send email in separate thread
        EmailThread(email).start()

        logger.info(
            f"Admin notification email queued for inquiry #{contact_inquiry.id}"
        )
        return True

    except Exception as e:
        logger.error(f"Error preparing admin notification email: {str(e)}")
        return False
