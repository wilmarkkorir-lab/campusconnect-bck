from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import StudyGroup, StudyGroupMember, StudySession, StudyGroupResource
from .serializers import (
    StudyGroupSerializer, StudyGroupMemberSerializer,
    StudySessionSerializer, StudyGroupResourceSerializer
)


class StudyGroupListView(generics.ListCreateAPIView):
    serializer_class = StudyGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course', 'is_private']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return StudyGroup.objects.filter(is_private=False)

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        StudyGroupMember.objects.create(group=group, user=self.request.user, role='admin')


class StudyGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        group = self.get_object()
        if not StudyGroupMember.objects.filter(group=group, user=request.user, role='admin').exists():
            return Response({'error': 'Only group admin can edit.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        if group.created_by != request.user:
            return Response({'error': 'Only creator can delete.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class MyStudyGroupsView(generics.ListAPIView):
    serializer_class = StudyGroupSerializer

    def get_queryset(self):
        member_group_ids = StudyGroupMember.objects.filter(
            user=self.request.user
        ).values_list('group_id', flat=True)
        return StudyGroup.objects.filter(id__in=member_group_ids)


class JoinStudyGroupView(APIView):
    def post(self, request, pk):
        group = generics.get_object_or_404(StudyGroup, pk=pk)
        if group.is_private:
            return Response({'error': 'This group is private.'}, status=status.HTTP_403_FORBIDDEN)
        current_count = StudyGroupMember.objects.filter(group=group).count()
        if current_count >= group.max_members:
            return Response({'error': 'Group is full.'}, status=status.HTTP_400_BAD_REQUEST)
        member, created = StudyGroupMember.objects.get_or_create(user=request.user, group=group)
        if not created:
            return Response({'error': 'Already a member.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Joined study group.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        StudyGroupMember.objects.filter(user=request.user, group_id=pk).delete()
        return Response({'message': 'Left study group.'})


class InviteMemberView(APIView):
    def post(self, request, pk):
        group = generics.get_object_or_404(StudyGroup, pk=pk)
        if not StudyGroupMember.objects.filter(group=group, user=request.user).exists():
            return Response({'error': 'You are not a member.'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        from accounts.models import User
        invited_user = generics.get_object_or_404(User, id=user_id)
        member, created = StudyGroupMember.objects.get_or_create(user=invited_user, group=group)
        if not created:
            return Response({'error': 'User is already a member.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f'{invited_user.full_name} added to group.'}, status=status.HTTP_201_CREATED)


class StudyGroupMembersView(generics.ListAPIView):
    serializer_class = StudyGroupMemberSerializer

    def get_queryset(self):
        return StudyGroupMember.objects.filter(group_id=self.kwargs['pk'])


class StudySessionListView(generics.ListCreateAPIView):
    serializer_class = StudySessionSerializer

    def get_queryset(self):
        return StudySession.objects.filter(group_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        group = generics.get_object_or_404(StudyGroup, pk=self.kwargs['pk'])
        serializer.save(group=group, created_by=self.request.user)


class StudySessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudySessionSerializer

    def get_queryset(self):
        return StudySession.objects.filter(group_id=self.kwargs['group_pk'])


class StudyGroupResourceListView(generics.ListCreateAPIView):
    serializer_class = StudyGroupResourceSerializer

    def get_queryset(self):
        return StudyGroupResource.objects.filter(group_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        group = generics.get_object_or_404(StudyGroup, pk=self.kwargs['pk'])
        serializer.save(group=group, uploaded_by=self.request.user)


class StudyGroupResourceDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = StudyGroupResourceSerializer

    def get_queryset(self):
        return StudyGroupResource.objects.filter(group_id=self.kwargs['group_pk'])
