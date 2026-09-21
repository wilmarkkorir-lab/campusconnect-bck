from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing_list'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('<int:listing_id>/save/', views.SaveListingView.as_view(), name='save_listing'),
    path('<int:listing_id>/images/', views.ListingImageUploadView.as_view(), name='listing_images'),
    path('saved/', views.SavedListingsView.as_view(), name='saved_listings'),
    path('my-listings/', views.MyListingsView.as_view(), name='my_listings'),
]
