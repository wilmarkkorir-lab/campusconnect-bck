from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import Announcement
from .serializers import AnnouncementSerializer
from accounts.permissions import IsLecturerOrAdmin


class AnnouncementListView(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'priority', 'university', 'department', 'course']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'priority']

    def get_queryset(self):
        now = timezone.now()
        return Announcement.objects.filter(
            is_published=True
        ).filter(
            models.Q(publish_at__isnull=True) | models.Q(publish_at__lte=now)
        ).filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gte=now)
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


# Fix missing import
from django.db import models
