from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Election, ElectionPosition, Candidate, Vote
from .serializers import ElectionSerializer, CandidateSerializer, VoteSerializer
from accounts.permissions import IsUniversityAdmin


class ElectionListView(generics.ListCreateAPIView):
    serializer_class = ElectionSerializer

    def get_queryset(self):
        return Election.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ElectionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Election.objects.filter(is_published=True)
    serializer_class = ElectionSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class NominateView(APIView):
    def post(self, request, position_id):
        position = generics.get_object_or_404(ElectionPosition, id=position_id)
        election = position.election
        now = timezone.now()
        if not (election.nomination_start <= now <= election.nomination_end):
            return Response({'error': 'Nominations are not open.'}, status=status.HTTP_400_BAD_REQUEST)
        if Candidate.objects.filter(position=position, user=request.user).exists():
            return Response({'error': 'Already nominated.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CastVoteView(APIView):
    def post(self, request, position_id):
        position = generics.get_object_or_404(ElectionPosition, id=position_id)
        election = position.election
        now = timezone.now()
        if not (election.voting_start <= now <= election.voting_end):
            return Response({'error': 'Voting is not open.'}, status=status.HTTP_400_BAD_REQUEST)
        if Vote.objects.filter(position=position, voter=request.user).exists():
            return Response({'error': 'Already voted for this position.'}, status=status.HTTP_400_BAD_REQUEST)
        candidate_id = request.data.get('candidate_id')
        candidate = generics.get_object_or_404(Candidate, id=candidate_id, position=position, status='approved')
        Vote.objects.create(position=position, voter=request.user, candidate=candidate)
        return Response({'message': 'Vote cast successfully.'})


class ApproveCandidateView(APIView):
    permission_classes = [IsUniversityAdmin]

    def post(self, request, candidate_id):
        candidate = generics.get_object_or_404(Candidate, id=candidate_id)
        candidate.status = request.data.get('status', 'approved')
        candidate.save()
        return Response(CandidateSerializer(candidate).data)
