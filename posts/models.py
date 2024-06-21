import uuid

from django.db import models
from django.db.models import ForeignKey

from accounts.models import UserAccount
from posts.utils import get_profile_image_upload_path, get_post_image_upload_path


class ProfilePic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_profile_image_upload_path)

    def __str__(self):
        return f"ProfilePic({self.id})"


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"Post({self.id})"


class PostPic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    image = models.ImageField(upload_to=get_post_image_upload_path)

    def __str__(self):
        return f"PostPic({self.id})"


class PostComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=True)
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    like_counter = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(UserAccount, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"PostComment({self.id})"
