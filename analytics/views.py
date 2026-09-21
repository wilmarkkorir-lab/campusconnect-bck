from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta

from .models import UserActivity, DailyStats
from accounts.permissions import IsUniversityAdmin
from accounts.models import User
from academics.models import Course, Material
from forum.models import ForumPost
from marketplace.models import MarketplaceListing
from jobs.models import Job
from events.models import Event
from messaging.models import Message


class AdminDashboardStatsView(APIView):
    permission_classes = [IsUniversityAdmin]

    def get(self, request):
        now = timezone.now()
        last_30 = now - timedelta(days=30)
        last_7 = now - timedelta(days=7)

        stats = {
            'users': {
                'total': User.objects.count(),
                'active': User.objects.filter(is_active=True).count(),
                'new_last_30_days': User.objects.filter(date_joined__gte=last_30).count(),
                'by_role': list(User.objects.values('role').annotate(count=Count('id'))),
            },
            'academics': {
                'total_courses': Course.objects.count(),
                'total_materials': Material.objects.count(),
                'materials_last_30_days': Material.objects.filter(created_at__gte=last_30).count(),
            },
            'community': {
                'total_forum_posts': ForumPost.objects.count(),
                'posts_last_7_days': ForumPost.objects.filter(created_at__gte=last_7).count(),
                'messages_last_7_days': Message.objects.filter(created_at__gte=last_7).count(),
            },
            'marketplace': {
                'total_listings': MarketplaceListing.objects.count(),
                'active_listings': MarketplaceListing.objects.filter(status='available').count(),
            },
            'opportunities': {
                'total_jobs': Job.objects.filter(is_published=True).count(),
                'total_events': Event.objects.filter(is_published=True).count(),
            },
        }
        return Response(stats)


class AdminDailyStatsView(generics.ListAPIView):
    permission_classes = [IsUniversityAdmin]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        since = timezone.now().date() - timedelta(days=days)
        stats = DailyStats.objects.filter(date__gte=since).order_by('date')
        data = list(stats.values())
        return Response(data)


class UserActivityListView(generics.ListAPIView):
    permission_classes = [IsUniversityAdmin]

    def get(self, request):
        days = int(request.query_params.get('days', 7))
        since = timezone.now() - timedelta(days=days)
        activities = (
            UserActivity.objects
            .filter(created_at__gte=since)
            .values('action')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response(list(activities))


class MyActivityView(generics.ListAPIView):
    def get(self, request):
        activities = UserActivity.objects.filter(user=request.user)[:50]
        data = list(activities.values('action', 'object_type', 'created_at'))
        return Response(data)


class LogActivityView(APIView):
    def post(self, request):
        action = request.data.get('action')
        if not action:
            return Response({'error': 'action required'}, status=400)
        UserActivity.objects.create(
            user=request.user,
            action=action,
            object_id=request.data.get('object_id'),
            object_type=request.data.get('object_type', ''),
            metadata=request.data.get('metadata', {}),
        )
        return Response({'logged': True})
