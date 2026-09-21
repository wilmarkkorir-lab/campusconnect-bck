from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course, Enrollment, Material, MaterialCategory, MaterialBookmark, Timetable, AcademicCalendar, PersonalReminder
from .serializers import (
    CourseSerializer, EnrollmentSerializer, MaterialSerializer,
    MaterialCategorySerializer, TimetableSerializer, AcademicCalendarSerializer, PersonalReminderSerializer
)
from accounts.permissions import IsLecturerOrAdmin, IsUniversityAdmin


class CourseListView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'year_of_study', 'semester', 'is_active', 'lecturer']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'created_at']

    def get_queryset(self):
        return Course.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class EnrollmentView(APIView):
    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
        serializer = EnrollmentSerializer(enrollments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=serializer.validated_data['course'],
            defaults={'is_active': True}
        )
        if not created:
            enrollment.is_active = True
            enrollment.save()
        return Response(EnrollmentSerializer(enrollment, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, course_id):
        Enrollment.objects.filter(student=request.user, course_id=course_id).update(is_active=False)
        return Response({'message': 'Unenrolled successfully.'})


class MaterialListView(generics.ListCreateAPIView):
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'material_type', 'category', 'is_approved']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'download_count']

    def get_queryset(self):
        return Material.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class MaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.download_count += 1
        instance.save(update_fields=['download_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MaterialBookmarkView(APIView):
    def post(self, request, material_id):
        material = generics.get_object_or_404(Material, id=material_id)
        bookmark, created = MaterialBookmark.objects.get_or_create(user=request.user, material=material)
        if not created:
            bookmark.delete()
            return Response({'bookmarked': False})
        return Response({'bookmarked': True})


class BookmarkedMaterialsView(generics.ListAPIView):
    serializer_class = MaterialSerializer

    def get_queryset(self):
        bookmarked_ids = MaterialBookmark.objects.filter(
            user=self.request.user
        ).values_list('material_id', flat=True)
        return Material.objects.filter(id__in=bookmarked_ids)


class TimetableListView(generics.ListCreateAPIView):
    serializer_class = TimetableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'day', 'semester']

    def get_queryset(self):
        user = self.request.user
        enrolled_courses = Enrollment.objects.filter(
            student=user, is_active=True
        ).values_list('course_id', flat=True)
        return Timetable.objects.filter(course_id__in=enrolled_courses)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class MaterialCategoryListView(generics.ListCreateAPIView):
    queryset = MaterialCategory.objects.all()
    serializer_class = MaterialCategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class AcademicCalendarListView(generics.ListCreateAPIView):
    serializer_class = AcademicCalendarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['university', 'event_type', 'semester', 'academic_year', 'is_published']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return AcademicCalendar.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AcademicCalendarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicCalendar.objects.all()
    serializer_class = AcademicCalendarSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class PersonalReminderView(generics.ListCreateAPIView):
    serializer_class = PersonalReminderSerializer

    def get_queryset(self):
        return PersonalReminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PersonalReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalReminderSerializer

    def get_queryset(self):
        return PersonalReminder.objects.filter(user=self.request.user)
