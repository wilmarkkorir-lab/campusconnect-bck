from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .models import University, Campus, Faculty, Department, Program, CampusLocation
from .serializers import (
    UniversitySerializer, UniversityListSerializer, CampusSerializer,
    FacultySerializer, DepartmentSerializer, ProgramSerializer, CampusLocationSerializer
)
from accounts.permissions import IsUniversityAdmin


class UniversityListView(generics.ListCreateAPIView):
    queryset = University.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['name', 'short_name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UniversityListSerializer
        return UniversitySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class CampusListView(generics.ListCreateAPIView):
    serializer_class = CampusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university']

    def get_queryset(self):
        return Campus.objects.filter(university_id=self.kwargs.get('university_id'))

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class FacultyListView(generics.ListCreateAPIView):
    serializer_class = FacultySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['university']
    search_fields = ['name', 'code']

    def get_queryset(self):
        return Faculty.objects.filter(university_id=self.kwargs.get('university_id'))

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class DepartmentListView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']

    def get_queryset(self):
        return Department.objects.filter(faculty__university_id=self.kwargs.get('university_id'))

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class ProgramListView(generics.ListCreateAPIView):
    serializer_class = ProgramSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['department', 'degree_type']
    search_fields = ['name', 'code']

    def get_queryset(self):
        return Program.objects.filter(department__faculty__university_id=self.kwargs.get('university_id'))

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class CampusLocationListView(generics.ListCreateAPIView):
    serializer_class = CampusLocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['campus', 'category']
    search_fields = ['name', 'building']

    def get_queryset(self):
        return CampusLocation.objects.filter(campus__university_id=self.kwargs.get('university_id'))

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class CampusMapView(generics.ListAPIView):
    """Returns all campus locations with coordinates for map rendering."""
    serializer_class = CampusLocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['campus', 'category']
    search_fields = ['name', 'building', 'description']

    def get_queryset(self):
        return CampusLocation.objects.filter(
            campus__university_id=self.kwargs.get('university_id'),
            campus__university__is_active=True,
        ).exclude(latitude=None, longitude=None)


class UniversityDirectoryView(generics.GenericAPIView):
    """Searchable directory of departments, offices and support services."""
    filter_backends = [SearchFilter]

    def get(self, request, university_id):
        search = request.query_params.get('search', '')
        faculties = Faculty.objects.filter(university_id=university_id)
        departments = Department.objects.filter(faculty__university_id=university_id)
        if search:
            faculties = faculties.filter(name__icontains=search)
            departments = departments.filter(name__icontains=search)
        return Response({
            'faculties': FacultySerializer(faculties, many=True).data,
            'departments': DepartmentSerializer(departments, many=True).data,
        })
