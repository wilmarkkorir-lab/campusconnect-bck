from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import FeeStructure
from .serializers import FeeStructureSerializer
from accounts.permissions import IsUniversityAdmin


class FeeStructureListView(generics.ListCreateAPIView):
    serializer_class = FeeStructureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'program', 'academic_year', 'semester', 'fee_type']

    def get_queryset(self):
        return FeeStructure.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeeStructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]
