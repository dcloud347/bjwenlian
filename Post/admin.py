from django.contrib import admin
from .models import Post,Comments
# Register your models here.

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'check', 'author','time_create')
    list_filter = ['title', 'check', 'author']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'reply_to', 'belonging', 'author','time_create')
    list_filter = ['reply_to', 'belonging', 'author']
