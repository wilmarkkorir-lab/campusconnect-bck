from django.db import models
from django.conf import settings


class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'forum_categories'
        verbose_name_plural = 'Forum Categories'

    def __str__(self):
        return self.name


class ForumPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_posts')
    category = models.ForeignKey(ForumCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    attachment = models.FileField(upload_to='forum/', null=True, blank=True)
    is_question = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'forum_posts'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    is_accepted_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.email} on {self.post.title}'


class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', '👍'), ('love', '❤️'), ('helpful', '💡'), ('funny', '😄'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, null=True, blank=True, related_name='reactions')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reactions'
        # Use unique_together instead of conditional constraints for MariaDB/MySQL compatibility
        unique_together = [('user', 'post'), ('user', 'comment')]


class PostBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_bookmarks'
        unique_together = ('user', 'post')
