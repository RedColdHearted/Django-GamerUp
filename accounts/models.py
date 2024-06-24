from rest_framework_simplejwt.tokens import RefreshToken

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

from app.utils import get_profile_image_upload_path, get_random_profile_picture


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

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
