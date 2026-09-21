from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
import secrets

from .models import Portfolio, Project, Certificate, Achievement, WorkExperience, Leadership
from .serializers import (
    PortfolioSerializer, ProjectSerializer, CertificateSerializer,
    AchievementSerializer, WorkExperienceSerializer, LeadershipSerializer
)


def get_or_create_portfolio(user):
    portfolio, created = Portfolio.objects.get_or_create(
        user=user,
        defaults={'share_token': secrets.token_urlsafe(32)}
    )
    return portfolio


class MyPortfolioView(generics.RetrieveUpdateAPIView):
    serializer_class = PortfolioSerializer

    def get_object(self):
        return get_or_create_portfolio(self.request.user)


class PublicPortfolioView(generics.RetrieveAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return generics.get_object_or_404(Portfolio, share_token=self.kwargs['token'], is_public=True)


class RegenerateShareTokenView(APIView):
    def post(self, request):
        portfolio = get_or_create_portfolio(request.user)
        portfolio.share_token = secrets.token_urlsafe(32)
        portfolio.save(update_fields=['share_token'])
        return Response({'share_token': portfolio.share_token})


class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(portfolio=get_or_create_portfolio(self.request.user))


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(portfolio__user=self.request.user)


class CertificateListView(generics.ListCreateAPIView):
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(portfolio=get_or_create_portfolio(self.request.user))


class CertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(portfolio__user=self.request.user)


class AchievementListView(generics.ListCreateAPIView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        return Achievement.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(portfolio=get_or_create_portfolio(self.request.user))


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        return Achievement.objects.filter(portfolio__user=self.request.user)


class WorkExperienceListView(generics.ListCreateAPIView):
    serializer_class = WorkExperienceSerializer

    def get_queryset(self):
        return WorkExperience.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(portfolio=get_or_create_portfolio(self.request.user))


class WorkExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer

    def get_queryset(self):
        return WorkExperience.objects.filter(portfolio__user=self.request.user)


class LeadershipListView(generics.ListCreateAPIView):
    serializer_class = LeadershipSerializer

    def get_queryset(self):
        return Leadership.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(portfolio=get_or_create_portfolio(self.request.user))


class LeadershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadershipSerializer

    def get_queryset(self):
        return Leadership.objects.filter(portfolio__user=self.request.user)
