from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Exam, ExamResult
from .serializers import ExamSerializer, ExamResultSerializer
from accounts.permissions import IsLecturerOrAdmin
from academics.models import Enrollment


class ExamListView(generics.ListCreateAPIView):
    serializer_class = ExamSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course', 'exam_type', 'semester', 'is_published']
    search_fields = ['title', 'course__code']

    def get_queryset(self):
        user = self.request.user
        enrolled_courses = Enrollment.objects.filter(
            student=user, is_active=True
        ).values_list('course_id', flat=True)
        return Exam.objects.filter(course_id__in=enrolled_courses, is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class MyExamResultsView(generics.ListAPIView):
    serializer_class = ExamResultSerializer

    def get_queryset(self):
        return ExamResult.objects.filter(student=self.request.user, is_published=True)


class ExamResultsAdminView(generics.ListCreateAPIView):
    serializer_class = ExamResultSerializer
    permission_classes = [IsLecturerOrAdmin]

    def get_queryset(self):
        return ExamResult.objects.filter(exam_id=self.kwargs['exam_id'])
