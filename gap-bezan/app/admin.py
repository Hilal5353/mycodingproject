from django.contrib import admin
from .models import Post, Profile, Comment, Reply, Followercount, PostReport
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Followercount)
admin.site.register(PostReport)



