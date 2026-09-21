from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import SportsTeam, TeamPlayer, Tournament, Fixture
from .serializers import SportsTeamSerializer, TeamPlayerSerializer, TournamentSerializer, FixtureSerializer
from accounts.permissions import IsUniversityAdmin


class SportsTeamListView(generics.ListCreateAPIView):
    serializer_class = SportsTeamSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['sport', 'university', 'is_active']
    search_fields = ['name', 'sport']

    def get_queryset(self):
        return SportsTeam.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class SportsTeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SportsTeam.objects.all()
    serializer_class = SportsTeamSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class TeamPlayersView(generics.ListCreateAPIView):
    serializer_class = TeamPlayerSerializer

    def get_queryset(self):
        return TeamPlayer.objects.filter(team_id=self.kwargs['team_id'])

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class TournamentListView(generics.ListCreateAPIView):
    serializer_class = TournamentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['sport', 'university', 'is_active']
    search_fields = ['name']

    def get_queryset(self):
        return Tournament.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class FixtureListView(generics.ListCreateAPIView):
    serializer_class = FixtureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament', 'status', 'home_team', 'away_team']

    def get_queryset(self):
        return Fixture.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class FixtureDetailView(generics.RetrieveUpdateAPIView):
    queryset = Fixture.objects.all()
    serializer_class = FixtureSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]
