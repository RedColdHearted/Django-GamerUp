from rest_framework import serializers

import posts.validators
from posts.models import Post, PostImage, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UsernameChangeSerializer(serializers.Serializer):
    """user's username serializer for UserViewSet"""
    username = serializers.CharField(max_length=150, validators=[posts.validators.validate_username])
