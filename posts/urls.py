from django.urls import path
from posts.views import LikeView, DeleteLikeView, DeletePostCommentView


app_name = "posts"

urlpatterns = [
    path("like/", LikeView.as_view(), name="like"),
    path("like/delete/", DeleteLikeView.as_view(), name="delete_like"),
    path('delete/comment/', DeletePostCommentView.as_view(), name="delete_com"),
]
