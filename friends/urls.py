from django.urls import path
from friends.views import FriendsChatView, FriendshipRequestView, CreateFriendshipRequestView, DontFriendshipView, ConfirmDeleteFriendshipView, DeleteFriendshipView, FriendsView, DeleteMessageView

app_name = "friends"

urlpatterns = [
    path('', FriendsView.as_view(), name="friends"),
    path("requests/", FriendshipRequestView.as_view(), name="friends_requests"),
    path('create/friendship/user/<int:id>/', CreateFriendshipRequestView.as_view(), name="create_friendship"),
    path('delete/request/<int:id>/', DontFriendshipView.as_view(), name="delete_request"),
    path("confirm/delete/friend/<int:id>/", ConfirmDeleteFriendshipView.as_view(), name="conf_del_friend"),
    path('delete/friend/<int:id>/', DeleteFriendshipView.as_view(), name="delete_friend"),
    path('chat/<int:id>/', FriendsChatView.as_view(), name="friends_chat"),
    path('<int:id>/delete/message/<int:msg_id>/', DeleteMessageView.as_view(), name="delete_message"),
]
