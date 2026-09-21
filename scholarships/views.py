from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Scholarship, SavedScholarship, ScholarshipApplication
from .serializers import ScholarshipSerializer, ScholarshipApplicationSerializer
from accounts.permissions import IsLecturerOrAdmin


class ScholarshipListView(generics.ListCreateAPIView):
    serializer_class = ScholarshipSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_fully_funded']
    search_fields = ['name', 'provider', 'description', 'eligibility']
    ordering_fields = ['deadline', 'created_at']

    def get_queryset(self):
        return Scholarship.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class ScholarshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scholarship.objects.filter(is_published=True)
    serializer_class = ScholarshipSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class SaveScholarshipView(APIView):
    def post(self, request, scholarship_id):
        scholarship = generics.get_object_or_404(Scholarship, id=scholarship_id)
        saved, created = SavedScholarship.objects.get_or_create(user=request.user, scholarship=scholarship)
        if not created:
            saved.delete()
            return Response({'saved': False})
        return Response({'saved': True})


class SavedScholarshipsView(generics.ListAPIView):
    serializer_class = ScholarshipSerializer

    def get_queryset(self):
        ids = SavedScholarship.objects.filter(user=self.request.user).values_list('scholarship_id', flat=True)
        return Scholarship.objects.filter(id__in=ids)


class ScholarshipApplicationView(generics.ListCreateAPIView):
    serializer_class = ScholarshipApplicationSerializer

    def get_queryset(self):
        return ScholarshipApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScholarshipApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ScholarshipApplicationSerializer

    def get_queryset(self):
        return ScholarshipApplication.objects.filter(user=self.request.user)
