from rest_framework import serializers
from .models import SportsTeam, TeamPlayer, Tournament, Fixture


class TeamPlayerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = TeamPlayer
        fields = '__all__'
        read_only_fields = ('joined_at',)


class SportsTeamSerializer(serializers.ModelSerializer):
    player_count = serializers.SerializerMethodField()

    class Meta:
        model = SportsTeam
        fields = '__all__'

    def get_player_count(self, obj):
        return obj.players.count()


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class FixtureSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)

    class Meta:
        model = Fixture
        fields = '__all__'
