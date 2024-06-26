from django.contrib import admin

from posts.models import Post, PostImage, Comment

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
