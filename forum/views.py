from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ForumCategory, ForumPost, Comment, Reaction, PostBookmark
from .serializers import ForumCategorySerializer, ForumPostSerializer, CommentSerializer
from accounts.permissions import IsUniversityAdmin


class ForumCategoryListView(generics.ListCreateAPIView):
    queryset = ForumCategory.objects.all()
    serializer_class = ForumCategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUniversityAdmin()]
        return [permissions.IsAuthenticated()]


class ForumPostListView(generics.ListCreateAPIView):
    serializer_class = ForumPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_question', 'is_answered', 'is_pinned']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count']

    def get_queryset(self):
        return ForumPost.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ForumPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumPost.objects.filter(is_published=True)
    serializer_class = ForumPostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        serializer.save()


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'], parent=None)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReactView(APIView):
    def post(self, request, post_id=None, comment_id=None):
        reaction_type = request.data.get('reaction_type', 'like')
        if post_id:
            post = generics.get_object_or_404(ForumPost, id=post_id)
            reaction, created = Reaction.objects.get_or_create(
                user=request.user, post=post, defaults={'reaction_type': reaction_type}
            )
        else:
            comment = generics.get_object_or_404(Comment, id=comment_id)
            reaction, created = Reaction.objects.get_or_create(
                user=request.user, comment=comment, defaults={'reaction_type': reaction_type}
            )
        if not created:
            reaction.delete()
            return Response({'reacted': False})
        return Response({'reacted': True, 'type': reaction_type})


class BookmarkPostView(APIView):
    def post(self, request, post_id):
        post = generics.get_object_or_404(ForumPost, id=post_id)
        bookmark, created = PostBookmark.objects.get_or_create(user=request.user, post=post)
        if not created:
            bookmark.delete()
            return Response({'bookmarked': False})
        return Response({'bookmarked': True})


class BookmarkedPostsView(generics.ListAPIView):
    serializer_class = ForumPostSerializer

    def get_queryset(self):
        ids = PostBookmark.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        return ForumPost.objects.filter(id__in=ids)
