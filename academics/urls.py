from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('enrollments/', views.EnrollmentView.as_view(), name='enrollments'),
    path('enrollments/<int:course_id>/', views.EnrollmentView.as_view(), name='unenroll'),
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('materials/<int:material_id>/bookmark/', views.MaterialBookmarkView.as_view(), name='material_bookmark'),
    path('materials/bookmarked/', views.BookmarkedMaterialsView.as_view(), name='bookmarked_materials'),
    path('timetable/', views.TimetableListView.as_view(), name='timetable'),
    path('material-categories/', views.MaterialCategoryListView.as_view(), name='material_categories'),
    path('calendar/', views.AcademicCalendarListView.as_view(), name='academic_calendar'),
    path('calendar/<int:pk>/', views.AcademicCalendarDetailView.as_view(), name='academic_calendar_detail'),
    path('reminders/', views.PersonalReminderView.as_view(), name='reminders'),
    path('reminders/<int:pk>/', views.PersonalReminderDetailView.as_view(), name='reminder_detail'),
]
