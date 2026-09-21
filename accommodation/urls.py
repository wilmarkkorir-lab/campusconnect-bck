from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccommodationListView.as_view(), name='accommodation_list'),
    path('<int:pk>/', views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('<int:accommodation_id>/images/', views.AccommodationImageUploadView.as_view(), name='accommodation_images'),
]
