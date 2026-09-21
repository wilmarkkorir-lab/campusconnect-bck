from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification, NotificationPreference


def send_notification(recipient, notification_type, title, message, link=''):
    """Create and push a real-time notification to a user."""
    prefs, _ = NotificationPreference.objects.get_or_create(user=recipient)
    pref_map = {
        'message': prefs.messages,
        'announcement': prefs.announcements,
        'assignment': prefs.assignments,
        'exam': prefs.exams,
        'event': prefs.events,
        'study_group': prefs.study_groups,
        'job': prefs.jobs,
        'scholarship': prefs.scholarships,
        'marketplace': prefs.marketplace,
    }
    if not pref_map.get(notification_type, True):
        return

    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{recipient.id}',
        {
            'type': 'send_notification',
            'data': {
                'id': notification.id,
                'notification_type': notification_type,
                'title': title,
                'message': message,
                'link': link,
                'created_at': notification.created_at.isoformat(),
            }
        }
    )

    if prefs.email_notifications:
        from accounts.tasks import send_notification_email
        send_notification_email.delay(recipient.email, title, message)
