from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Report, ModerationLog
from .serializers import ReportSerializer, ReportAdminSerializer, ModerationLogSerializer
from accounts.permissions import IsUniversityAdmin


class SubmitReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)


class MyReportsView(generics.ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        return Report.objects.filter(reported_by=self.request.user)


class AdminReportListView(generics.ListAPIView):
    serializer_class = ReportAdminSerializer
    permission_classes = [IsUniversityAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'report_type', 'content_type', 'action_taken']
    search_fields = ['description']
    ordering_fields = ['created_at', 'status']
    queryset = Report.objects.all()


class AdminReportDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ReportAdminSerializer
    permission_classes = [IsUniversityAdmin]
    queryset = Report.objects.all()


class ModerateReportView(APIView):
    permission_classes = [IsUniversityAdmin]

    def post(self, request, pk):
        report = generics.get_object_or_404(Report, pk=pk)
        action = request.data.get('action', 'none')
        notes = request.data.get('notes', '')
        new_status = request.data.get('status', 'resolved')

        report.action_taken = action
        report.status = new_status
        report.reviewed_by = request.user
        report.admin_notes = notes
        report.save()

        ModerationLog.objects.create(
            report=report,
            moderator=request.user,
            action=action,
            notes=notes
        )
        return Response(ReportAdminSerializer(report).data)
