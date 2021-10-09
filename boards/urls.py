from django.urls import path
from .views import HomeView, ReplyTopicView, EditPostView, about, board_detail, new_topic, topic_posts

app_name = 'boards'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('boards/<str:board_name>/', board_detail, name='board_detail'),
    path('boards/<str:board_name>/new/', new_topic, name='new_topic'),
    path('boards/<str:board_name>/topics/<int:pk>/', topic_posts, name='topic_posts'),
    path('boards/<str:board_name>/topics/<int:pk>/reply/', ReplyTopicView.as_view(), name='reply_topic'),
    path('boards/<str:board_name>/topics/<int:pk>/posts/<int:post_pk>/edit/', EditPostView.as_view(), name='edit_post'),
]
