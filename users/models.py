from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="default_profile_pic.jpg")


# class FriendshipRequest(models.Model):
#     to_user = models.ForeignKey('auth.User',on_delete=models.CASCADE related_name="friendship_requests_to")
#     from_user = models.ForeignKey('auth.User', related_name="friendship_requests_from")
#     status = models.CharField(max_length=25, default='CREATED')
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"ОТ {self.from_user.first_name} ({self.from_user.last_name} К {self.to_user.first_name} {self.to_user.last_name})"
    

# class Friendship(models.Model):
#     to_user = models.ForeignKey(CustomUser, related_name="friends", on_delete=models.CASCADE)
#     from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.to_user.first_name} ({self.to_user.last_name} И {self.from_user.first_name} {self.from_user.last_name})"