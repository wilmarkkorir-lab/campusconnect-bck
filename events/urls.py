from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:event_id>/register/', views.EventRegisterView.as_view(), name='event_register'),
    path('<int:event_id>/attendees/', views.EventAttendeesView.as_view(), name='event_attendees'),
    path('checkin/', views.QRCheckInView.as_view(), name='qr_checkin'),
    path('my-registrations/', views.MyEventRegistrationsView.as_view(), name='my_event_registrations'),
]
