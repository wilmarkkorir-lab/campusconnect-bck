from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClubListView.as_view(), name='club_list'),
    path('<int:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('<int:club_id>/join/', views.ClubMembershipView.as_view(), name='club_join'),
    path('<int:club_id>/members/', views.ClubMembersView.as_view(), name='club_members'),
    path('<int:club_id>/announcements/', views.ClubAnnouncementListView.as_view(), name='club_announcements'),
]
