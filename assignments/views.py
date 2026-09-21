from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSubmissionSerializer
from accounts.permissions import IsLecturerOrAdmin


class AssignmentListView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course', 'is_published']
    search_fields = ['title']

    def get_queryset(self):
        return Assignment.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class SubmitAssignmentView(APIView):
    def post(self, request, assignment_id):
        assignment = generics.get_object_or_404(Assignment, id=assignment_id)
        if not assignment.allow_submissions:
            return Response({'error': 'Submissions are closed.'}, status=status.HTTP_400_BAD_REQUEST)
        is_late = timezone.now() > assignment.deadline
        submission, created = Submission.objects.get_or_create(
            assignment=assignment, student=request.user,
            defaults={
                'file': request.FILES.get('file'),
                'text_response': request.data.get('text_response', ''),
                'status': 'late' if is_late else 'submitted'
            }
        )
        if not created:
            submission.file = request.FILES.get('file', submission.file)
            submission.text_response = request.data.get('text_response', submission.text_response)
            submission.status = 'late' if is_late else 'submitted'
            submission.save()
        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)


class AssignmentSubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsLecturerOrAdmin]

    def get_queryset(self):
        return Submission.objects.filter(assignment_id=self.kwargs['assignment_id'])


class GradeSubmissionView(APIView):
    permission_classes = [IsLecturerOrAdmin]

    def post(self, request, submission_id):
        submission = generics.get_object_or_404(Submission, id=submission_id)
        serializer = GradeSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission.marks_obtained = serializer.validated_data['marks_obtained']
        submission.feedback = serializer.validated_data.get('feedback', '')
        submission.status = 'graded'
        submission.graded_by = request.user
        submission.graded_at = timezone.now()
        submission.save()
        return Response(SubmissionSerializer(submission).data)


class MySubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)
