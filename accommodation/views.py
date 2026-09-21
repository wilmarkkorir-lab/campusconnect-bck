from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Accommodation, AccommodationImage
from .serializers import AccommodationSerializer
from accounts.permissions import IsLecturerOrAdmin


class AccommodationListView(generics.ListCreateAPIView):
    serializer_class = AccommodationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['accommodation_type', 'university', 'is_available']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_month', 'created_at']

    def get_queryset(self):
        return Accommodation.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class AccommodationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accommodation.objects.filter(is_published=True)
    serializer_class = AccommodationSerializer

    def perform_update(self, serializer):
        acc = self.get_object()
        if acc.posted_by != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if instance.posted_by != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        instance.is_published = False
        instance.save()


class AccommodationImageUploadView(APIView):
    def post(self, request, accommodation_id):
        acc = generics.get_object_or_404(Accommodation, id=accommodation_id, posted_by=request.user)
        images = request.FILES.getlist('images')
        for img in images:
            AccommodationImage.objects.create(accommodation=acc, image=img)
        return Response({'message': f'{len(images)} image(s) uploaded.'}, status=status.HTTP_201_CREATED)
