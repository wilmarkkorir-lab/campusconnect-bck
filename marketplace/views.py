from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MarketplaceListing, ListingImage, SavedListing
from .serializers import MarketplaceListingSerializer


class ListingListView(generics.ListCreateAPIView):
    serializer_class = MarketplaceListingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        return MarketplaceListing.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketplaceListing.objects.filter(is_published=True)
    serializer_class = MarketplaceListingSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        listing = self.get_object()
        if listing.seller != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if instance.seller != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        instance.is_published = False
        instance.save()


class SaveListingView(APIView):
    def post(self, request, listing_id):
        listing = generics.get_object_or_404(MarketplaceListing, id=listing_id)
        saved, created = SavedListing.objects.get_or_create(user=request.user, listing=listing)
        if not created:
            saved.delete()
            return Response({'saved': False})
        return Response({'saved': True})


class SavedListingsView(generics.ListAPIView):
    serializer_class = MarketplaceListingSerializer

    def get_queryset(self):
        ids = SavedListing.objects.filter(user=self.request.user).values_list('listing_id', flat=True)
        return MarketplaceListing.objects.filter(id__in=ids)


class MyListingsView(generics.ListAPIView):
    serializer_class = MarketplaceListingSerializer

    def get_queryset(self):
        return MarketplaceListing.objects.filter(seller=self.request.user)


class ListingImageUploadView(APIView):
    def post(self, request, listing_id):
        listing = generics.get_object_or_404(MarketplaceListing, id=listing_id, seller=request.user)
        images = request.FILES.getlist('images')
        for img in images:
            ListingImage.objects.create(listing=listing, image=img)
        return Response({'message': f'{len(images)} image(s) uploaded.'}, status=status.HTTP_201_CREATED)
