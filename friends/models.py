from django.utils import timezone
from django.db import models

from users.models import CustomUser

# Create your models here.

class FriendshipRequest(models.Model):
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friendship_requests_to")
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friendship_requests_from")
    created_at = models.DateTimeField(default=timezone.now)
    view = models.BooleanField(default=False)

    def __str__(self):
        return f"ОТ {self.from_user.username} К {self.to_user.username}"
    

class Friendship(models.Model):
    to_user = models.ForeignKey(CustomUser, related_name="friends_to", on_delete=models.CASCADE)
    from_user = models.ForeignKey(CustomUser,related_name="friends_from", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.to_user.username } И {self.from_user.username}"
    

class FriendChat(models.Model):
    friends = models.ForeignKey(Friendship, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"От {self.user} в чат"
    