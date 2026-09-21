from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeeStructureListView.as_view(), name='fee_list'),
    path('<int:pk>/', views.FeeStructureDetailView.as_view(), name='fee_detail'),
]
