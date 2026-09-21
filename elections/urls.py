from django.urls import path
from . import views

urlpatterns = [
    path('', views.ElectionListView.as_view(), name='election_list'),
    path('<int:pk>/', views.ElectionDetailView.as_view(), name='election_detail'),
    path('positions/<int:position_id>/nominate/', views.NominateView.as_view(), name='nominate'),
    path('positions/<int:position_id>/vote/', views.CastVoteView.as_view(), name='cast_vote'),
    path('candidates/<int:candidate_id>/approve/', views.ApproveCandidateView.as_view(), name='approve_candidate'),
]
