from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from academics.models import Enrollment, Timetable
from assignments.models import Assignment, Submission
from exams.models import Exam
from notifications.models import Notification
from messaging.models import Conversation
from events.models import Event, EventRegistration
from jobs.models import Job
from scholarships.models import Scholarship
from announcements.models import Announcement


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        now = timezone.now()
        today = now.date()
        week_ahead = today + timedelta(days=7)

        enrolled_course_ids = Enrollment.objects.filter(
            student=user, is_active=True
        ).values_list('course_id', flat=True)

        # Upcoming timetable entries (today's classes)
        day_name = today.strftime('%A').lower()
        upcoming_classes = list(
            Timetable.objects.filter(course_id__in=enrolled_course_ids, day=day_name)
            .select_related('course')
            .values('course__code', 'course__name', 'start_time', 'end_time', 'venue')[:5]
        )

        # Upcoming assignment deadlines
        submitted_ids = Submission.objects.filter(student=user).values_list('assignment_id', flat=True)
        upcoming_assignments = list(
            Assignment.objects.filter(
                course_id__in=enrolled_course_ids,
                deadline__gte=now,
                deadline__date__lte=week_ahead,
                is_published=True,
            ).exclude(id__in=submitted_ids)
            .values('id', 'title', 'deadline', 'course__code')
            .order_by('deadline')[:5]
        )

        # Upcoming exams
        upcoming_exams = list(
            Exam.objects.filter(
                course_id__in=enrolled_course_ids,
                date__gte=today,
                date__lte=week_ahead,
                is_published=True,
            ).values('id', 'title', 'exam_type', 'date', 'start_time', 'venue', 'course__code')
            .order_by('date', 'start_time')[:5]
        )

        # Unread notifications count
        unread_notifications = Notification.objects.filter(
            recipient=user, is_read=False
        ).count()

        # Unread messages count
        unread_messages = 0
        for conv in Conversation.objects.filter(participants=user):
            unread_messages += conv.messages.filter(is_read=False).exclude(sender=user).count()

        # Upcoming registered events
        upcoming_events = list(
            Event.objects.filter(
                registrations__user=user,
                start_datetime__gte=now,
                start_datetime__date__lte=week_ahead,
            ).values('id', 'title', 'start_datetime', 'location', 'event_type')
            .order_by('start_datetime')[:5]
        )

        # Recent announcements
        recent_announcements = list(
            Announcement.objects.filter(is_published=True)
            .values('id', 'title', 'category', 'priority', 'created_at')
            .order_by('-created_at')[:5]
        )

        # Recommended: latest jobs and scholarships
        latest_jobs = list(
            Job.objects.filter(is_published=True)
            .values('id', 'title', 'organization', 'job_type', 'deadline')
            .order_by('-created_at')[:3]
        )
        latest_scholarships = list(
            Scholarship.objects.filter(is_published=True)
            .values('id', 'name', 'provider', 'deadline', 'is_fully_funded')
            .order_by('-created_at')[:3]
        )

        return Response({
            'upcoming_classes': upcoming_classes,
            'upcoming_assignments': upcoming_assignments,
            'upcoming_exams': upcoming_exams,
            'unread_notifications': unread_notifications,
            'unread_messages': unread_messages,
            'upcoming_events': upcoming_events,
            'recent_announcements': recent_announcements,
            'latest_jobs': latest_jobs,
            'latest_scholarships': latest_scholarships,
            'enrolled_courses_count': len(enrolled_course_ids),
        })
