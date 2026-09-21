from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(email, code, purpose):
    subjects = {
        'email_verify': 'Verify Your CampusConnect Email',
        'password_reset': 'CampusConnect Password Reset Code',
        'two_factor': 'CampusConnect Two-Factor Authentication Code',
    }
    messages = {
        'email_verify': f'Your email verification code is: {code}\nThis code expires in 10 minutes.',
        'password_reset': f'Your password reset code is: {code}\nThis code expires in 15 minutes.',
        'two_factor': f'Your 2FA code is: {code}\nThis code expires in 5 minutes.',
    }
    send_mail(
        subject=subjects.get(purpose, 'CampusConnect Code'),
        message=messages.get(purpose, f'Your code is: {code}'),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def send_notification_email(email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )
