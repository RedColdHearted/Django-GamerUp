from django.contrib import admin

from posts.models import ProfilePic, Post, PostPic, PostComment

admin.site.register(ProfilePic)
admin.site.register(Post)
admin.site.register(PostPic)
admin.site.register(PostComment)
