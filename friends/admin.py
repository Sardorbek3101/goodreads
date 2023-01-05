from django.contrib import admin
from friends.models import FriendshipRequest, Friendship, FriendChat


admin.site.register(FriendshipRequest)
admin.site.register(Friendship)
admin.site.register(FriendChat)
