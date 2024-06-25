import uuid

from django.db import models

from accounts.models import UserAccount
from app.utils import get_post_image_upload_path
from posts.validators import validate_zero_or_more


class Post(models.Model):
    class Meta:
        ordering = ['created_at']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, blank=True)
    content = models.TextField()
    views = models.IntegerField(default=0)
    like_counter = models.IntegerField(default=0, validators=[validate_zero_or_more])
    liked_by = models.ManyToManyField(UserAccount, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post({self.id})"


class PostPic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    image = models.ImageField(upload_to=get_post_image_upload_path)

    def __str__(self):
        return f"PostPic({self.id})"


class PostComment(models.Model):
    class Meta:
        ordering = ['like_counter']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=True)
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    like_counter = models.IntegerField(default=0, validators=[validate_zero_or_more])
    liked_by = models.ManyToManyField(UserAccount, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"PostComment({self.id})"
