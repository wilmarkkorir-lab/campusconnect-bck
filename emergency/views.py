from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import EmergencyContact, EmergencyAnnouncement, IncidentReport
from .serializers import EmergencyContactSerializer, EmergencyAnnouncementSerializer, IncidentReportSerializer
from accounts.permissions import IsUniversityAdmin


class EmergencyContactListView(generics.ListCreateAPIView):
    serializer_class = EmergencyContactSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'contact_type', 'is_active']

    def get_queryset(self):
        return EmergencyContact.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class EmergencyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class EmergencyAnnouncementListView(generics.ListCreateAPIView):
    serializer_class = EmergencyAnnouncementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'is_active']

    def get_queryset(self):
        return EmergencyAnnouncement.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EmergencyAnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyAnnouncement.objects.all()
    serializer_class = EmergencyAnnouncementSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class IncidentReportListView(generics.ListCreateAPIView):
    serializer_class = IncidentReportSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['university_admin', 'super_admin']:
            return IncidentReport.objects.all()
        return IncidentReport.objects.filter(reported_by=user)

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)


class IncidentReportDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IncidentReportSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['university_admin', 'super_admin']:
            return IncidentReport.objects.all()
        return IncidentReport.objects.filter(reported_by=user)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]
