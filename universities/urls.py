from django.urls import path
from . import views

urlpatterns = [
    path('', views.UniversityListView.as_view(), name='university_list'),
    path('<int:pk>/', views.UniversityDetailView.as_view(), name='university_detail'),
    path('<int:university_id>/campuses/', views.CampusListView.as_view(), name='campus_list'),
    path('<int:university_id>/faculties/', views.FacultyListView.as_view(), name='faculty_list'),
    path('<int:university_id>/departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('<int:university_id>/programs/', views.ProgramListView.as_view(), name='program_list'),
    # Campus directory & map
    path('<int:university_id>/locations/', views.CampusLocationListView.as_view(), name='location_list'),
    path('<int:university_id>/map/', views.CampusMapView.as_view(), name='campus_map'),
    path('<int:university_id>/directory/', views.UniversityDirectoryView.as_view(), name='university_directory'),
]
