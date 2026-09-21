from rest_framework import serializers
from .models import ForumCategory, ForumPost, Comment, Reaction, PostBookmark


class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    replies = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'created_at')

    def get_replies(self, obj):
        if obj.parent is None:
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []

    def get_reaction_count(self, obj):
        return obj.reactions.count()


class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    comment_count = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = '__all__'
        read_only_fields = ('author', 'views_count', 'created_at')

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_reaction_count(self, obj):
        return obj.reactions.count()

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostBookmark.objects.filter(user=request.user, post=obj).exists()
        return False
