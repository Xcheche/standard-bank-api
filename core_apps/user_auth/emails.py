from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from django.core.mail import EmailMultiAlternatives
from loguru import logger


def send_otp_email(email, otp):
    subject = _("Your OTP Code for Login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    context = {
        'otp': otp,
        'expiry_time': settings.OTP_EXPIRATION,
        'site_name': settings.SITE_NAME
    }
    html_email = render_to_string('emails/otp_email.html', context)
    plain_message = strip_tags(html_email)
    email_obj = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
    email_obj.attach_alternative(html_email, "text/html")
    try:
        email_obj.send()
        logger.info(f"OTP email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")


def send_account_locked_email(email, user):
    subject = _("Your Account Has Been Locked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    context = {
        'user': user,
        'site_name': settings.SITE_NAME,
        'lock_duration': int(settings.LOGOUT_DURATION.total_seconds() // 60)  # Convert to minutes
    }
    html_email = render_to_string('emails/account_locked.html', context)
    plain_message = strip_tags(html_email)
    email_obj = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
    email_obj.attach_alternative(html_email, "text/html")
    try:
        email_obj.send()
        logger.info(f"Account locked email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send account locked email to {email}: {e}")
