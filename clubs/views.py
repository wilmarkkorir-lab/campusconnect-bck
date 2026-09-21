from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Club, ClubMember, ClubAnnouncement
from .serializers import ClubSerializer, ClubMemberSerializer, ClubAnnouncementSerializer
from accounts.permissions import IsUniversityAdmin


class ClubListView(generics.ListCreateAPIView):
    serializer_class = ClubSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['club_type', 'university', 'is_active']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return Club.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClubDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class ClubMembershipView(APIView):
    def post(self, request, club_id):
        club = generics.get_object_or_404(Club, id=club_id)
        member, created = ClubMember.objects.get_or_create(user=request.user, club=club)
        if not created:
            return Response({'error': 'Already a member.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Joined club.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, club_id):
        ClubMember.objects.filter(user=request.user, club_id=club_id).delete()
        return Response({'message': 'Left club.'})


class ClubMembersView(generics.ListAPIView):
    serializer_class = ClubMemberSerializer

    def get_queryset(self):
        return ClubMember.objects.filter(club_id=self.kwargs['club_id'])


class ClubAnnouncementListView(generics.ListCreateAPIView):
    serializer_class = ClubAnnouncementSerializer

    def get_queryset(self):
        return ClubAnnouncement.objects.filter(club_id=self.kwargs['club_id'])

    def perform_create(self, serializer):
        club = generics.get_object_or_404(Club, id=self.kwargs['club_id'])
        serializer.save(created_by=self.request.user, club=club)
