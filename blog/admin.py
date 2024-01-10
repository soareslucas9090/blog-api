from django.contrib import admin

from .models import *


@admin.register(User)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "email",
        "description",
        "is_author",
        "is_admin",
        "is_active",
        "is_staff",
        "is_superuser",
    ]


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
