from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ForumCategoryListView.as_view(), name='forum_categories'),
    path('posts/', views.ForumPostListView.as_view(), name='forum_posts'),
    path('posts/<int:pk>/', views.ForumPostDetailView.as_view(), name='forum_post_detail'),
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='post_comments'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('posts/<int:post_id>/react/', views.ReactView.as_view(), name='react_post'),
    path('comments/<int:comment_id>/react/', views.ReactView.as_view(), name='react_comment'),
    path('posts/<int:post_id>/bookmark/', views.BookmarkPostView.as_view(), name='bookmark_post'),
    path('bookmarks/', views.BookmarkedPostsView.as_view(), name='bookmarked_posts'),
]
