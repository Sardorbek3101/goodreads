from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="default_profile_pic.jpg")


# class RequestFriends(models.Model):
#     from_whom = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     to_whom = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"ОТ {self.from_whom.first_name} ({self.from_whom.last_name} К {self.to_whom.first_name} {self.to_whom.last_name})"
    

# class Friends(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.send_friend.first_name} ({self.send_friend.last_name} И {self.receive_friend.first_name} {self.receive_friend.last_name})"
    