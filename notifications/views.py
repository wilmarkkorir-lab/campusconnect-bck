from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class MarkNotificationReadView(APIView):
    def post(self, request, pk=None):
        if pk:
            Notification.objects.filter(id=pk, recipient=request.user).update(is_read=True)
        else:
            Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'Marked as read.'})


class UnreadCountView(APIView):
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'unread_count': count})


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer

    def get_object(self):
        prefs, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return prefs
