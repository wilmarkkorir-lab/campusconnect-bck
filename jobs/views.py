from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from accounts.permissions import IsLecturerOrAdmin


class JobListView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['job_type', 'is_remote']
    search_fields = ['title', 'organization', 'description']
    ordering_fields = ['deadline', 'created_at']

    def get_queryset(self):
        return Job.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.filter(is_published=True)
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class JobApplyView(APIView):
    def post(self, request, job_id):
        job = generics.get_object_or_404(Job, id=job_id, is_published=True)
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response({'error': 'Already applied.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = JobApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(job=job, applicant=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)


class JobApplicationsAdminView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsLecturerOrAdmin]

    def get_queryset(self):
        return JobApplication.objects.filter(job_id=self.kwargs['job_id'])
