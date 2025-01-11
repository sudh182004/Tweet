from django.contrib import admin
from .models import Tweet, Comments, Like

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at", "like_count", "comment_count")
    search_fields = ("user__username", "content")

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "tweet", "content", "created_at")
    search_fields = ("user__username", "content")

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "tweet", "created_at")
    search_fields = ("user__username",)
