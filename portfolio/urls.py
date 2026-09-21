from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyPortfolioView.as_view(), name='my_portfolio'),
    path('share/<str:token>/', views.PublicPortfolioView.as_view(), name='public_portfolio'),
    path('regenerate-token/', views.RegenerateShareTokenView.as_view(), name='regenerate_token'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('certificates/', views.CertificateListView.as_view(), name='certificate_list'),
    path('certificates/<int:pk>/', views.CertificateDetailView.as_view(), name='certificate_detail'),
    path('achievements/', views.AchievementListView.as_view(), name='achievement_list'),
    path('achievements/<int:pk>/', views.AchievementDetailView.as_view(), name='achievement_detail'),
    path('work-experience/', views.WorkExperienceListView.as_view(), name='work_experience_list'),
    path('work-experience/<int:pk>/', views.WorkExperienceDetailView.as_view(), name='work_experience_detail'),
    path('leadership/', views.LeadershipListView.as_view(), name='leadership_list'),
    path('leadership/<int:pk>/', views.LeadershipDetailView.as_view(), name='leadership_detail'),
]
