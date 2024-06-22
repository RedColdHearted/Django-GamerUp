from django.contrib import admin

from posts.models import Post, PostPic, PostComment

admin.site.register(Post)
admin.site.register(PostPic)
admin.site.register(PostComment)
