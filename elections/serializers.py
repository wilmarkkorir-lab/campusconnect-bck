from rest_framework import serializers
from .models import Election, ElectionPosition, Candidate, Vote


class CandidateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at')

    def get_vote_count(self, obj):
        election = obj.position.election
        if election.status == 'results_published':
            return obj.votes_received.count()
        return None


class ElectionPositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = ElectionPosition
        fields = '__all__'


class ElectionSerializer(serializers.ModelSerializer):
    positions = ElectionPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ('voter', 'voted_at')
