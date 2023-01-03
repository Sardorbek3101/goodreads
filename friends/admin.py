from django.contrib import admin
from friends.models import FriendshipRequest, Friendship


admin.site.register(FriendshipRequest)
admin.site.register(Friendship)
