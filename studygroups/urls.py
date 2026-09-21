from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudyGroupListView.as_view(), name='study_group_list'),
    path('mine/', views.MyStudyGroupsView.as_view(), name='my_study_groups'),
    path('<int:pk>/', views.StudyGroupDetailView.as_view(), name='study_group_detail'),
    path('<int:pk>/join/', views.JoinStudyGroupView.as_view(), name='join_study_group'),
    path('<int:pk>/invite/', views.InviteMemberView.as_view(), name='invite_member'),
    path('<int:pk>/members/', views.StudyGroupMembersView.as_view(), name='study_group_members'),
    path('<int:pk>/sessions/', views.StudySessionListView.as_view(), name='study_session_list'),
    path('<int:group_pk>/sessions/<int:pk>/', views.StudySessionDetailView.as_view(), name='study_session_detail'),
    path('<int:pk>/resources/', views.StudyGroupResourceListView.as_view(), name='study_group_resources'),
    path('<int:group_pk>/resources/<int:pk>/', views.StudyGroupResourceDetailView.as_view(), name='study_group_resource_detail'),
]
