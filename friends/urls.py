from django.urls import path
from friends.views import FriendshipRequestView, CreateFriendshipRequestView, ConfirmFriendshipView, ConfirmDeleteFriendshipView, DeleteFriendshipView, FriendsView

app_name = "friends"

urlpatterns = [
    path('', FriendsView.as_view(), name="friends"),
    path("requests/", FriendshipRequestView.as_view(), name="friends_requests"),
    path('create/friendship/user/<int:id>/', CreateFriendshipRequestView.as_view(), name="create_friendship"),
    path('confirm/friendhip/<int:id>/', ConfirmFriendshipView.as_view(), name="confirm_friendship"),
    path("confirm/delete/friend/<int:id>/", ConfirmDeleteFriendshipView.as_view(), name="conf_del_friend"),
    path('delete/friend/<int:id>/', DeleteFriendshipView.as_view(), name="delete_friend")
]
