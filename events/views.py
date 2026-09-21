from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from accounts.permissions import IsLecturerOrAdmin


class EventListView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event_type', 'university', 'club', 'is_online']
    search_fields = ['title', 'description']
    ordering_fields = ['start_datetime', 'created_at']

    def get_queryset(self):
        return Event.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_published=True)
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


class EventRegisterView(APIView):
    def post(self, request, event_id):
        event = generics.get_object_or_404(Event, id=event_id, is_published=True)
        if event.max_attendees:
            count = event.registrations.filter(status='registered').count()
            if count >= event.max_attendees:
                return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)
        reg, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
        if not created:
            return Response({'error': 'Already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(EventRegistrationSerializer(reg).data, status=status.HTTP_201_CREATED)

    def delete(self, request, event_id):
        EventRegistration.objects.filter(user=request.user, event_id=event_id).update(status='cancelled')
        return Response({'message': 'Registration cancelled.'})


class EventAttendeesView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsLecturerOrAdmin]

    def get_queryset(self):
        return EventRegistration.objects.filter(event_id=self.kwargs['event_id'])


class QRCheckInView(APIView):
    permission_classes = [IsLecturerOrAdmin]

    def post(self, request):
        qr_code = request.data.get('qr_code')
        try:
            reg = EventRegistration.objects.get(qr_code=qr_code)
            reg.status = 'attended'
            reg.save()
            return Response({'message': f'{reg.user.full_name} checked in to {reg.event.title}.'})
        except EventRegistration.DoesNotExist:
            return Response({'error': 'Invalid QR code.'}, status=status.HTTP_400_BAD_REQUEST)


class MyEventRegistrationsView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)
