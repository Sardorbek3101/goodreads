from mimetypes import guess_type
from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Posts(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='videos_uploaded',null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(CustomUser, related_name="likes", blank=True)
    
    def __str__(self):
        return self.title


class PostComments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Пользователь {self.user} прокоментировал {self.post.title}"
