import os
from datetime import datetime, timedelta, timezone

from rest_framework_simplejwt.tokens import RefreshToken

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.timezone import now

from app.utils import get_profile_image_upload_path, get_random_profile_picture, is_not_default_pic
from app.exceptions import UsernameException


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.image = get_random_profile_picture()
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    username_last_updated_at = models.DateTimeField(default=now, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_profile_image_upload_path, blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} id - {self.id}"

    @staticmethod
    def in_test_api_auth(client, jwt_token):
        """authorize user, creating Authorization header with jwt_token (using for tests)"""
        client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt_token)

    def get_jwt_token_for_user(self):
        """creating access jwt token for user"""
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def set_username(self, new_username):
        """Set a username if 3 days have passed since the username was changed"""
        current_date = datetime.now(timezone.utc)
        difference = current_date - self.username_last_updated_at
        if difference < timedelta(days=3):
            raise UsernameException('less than 3 days have passed since the username was changed')
        else:
            self.username = new_username
            self.save()

    def set_image(self, new_image):
        """Set a new user image and delete old if it not a default"""
        if self.image:
            old_avatar_path = self.image.path
            old_avatar_name = self.image.name.split('/')[1]
            if is_not_default_pic(old_avatar_name):
                os.remove(old_avatar_path)

        self.image = new_image
        self.save()

    def get_image(self):
        """Get user image"""
        return self.image

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
