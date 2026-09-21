from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/auth/', include('accounts.urls')),
    path('api/universities/', include('universities.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/forum/', include('forum.urls')),
    path('api/messaging/', include('messaging.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/study-groups/', include('studygroups.urls')),
    path('api/clubs/', include('clubs.urls')),
    path('api/sports/', include('sports.urls')),
    path('api/events/', include('events.urls')),
    path('api/marketplace/', include('marketplace.urls')),
    path('api/accommodation/', include('accommodation.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/scholarships/', include('scholarships.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/elections/', include('elections.urls')),
    path('api/emergency/', include('emergency.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/finance/', include('finance.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
