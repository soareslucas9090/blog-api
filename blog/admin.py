from django.contrib import admin

from .models import *


@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "description", "is_author", "email"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "tittle",
        "content",
        "created_at",
        "updated_at",
        "is_visible",
        "author",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user", "text", "created_at"]
