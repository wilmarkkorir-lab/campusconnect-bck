from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.SportsTeamListView.as_view(), name='sports_team_list'),
    path('teams/<int:pk>/', views.SportsTeamDetailView.as_view(), name='sports_team_detail'),
    path('teams/<int:team_id>/players/', views.TeamPlayersView.as_view(), name='team_players'),
    path('tournaments/', views.TournamentListView.as_view(), name='tournament_list'),
    path('fixtures/', views.FixtureListView.as_view(), name='fixture_list'),
    path('fixtures/<int:pk>/', views.FixtureDetailView.as_view(), name='fixture_detail'),
]
