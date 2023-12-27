from models import *
from rest_framework import serializers


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ["id", "name", "description", "is_author", "email"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "tittle",
            "content",
            "created_at",
            "edited_at",
            "updated_at",
            "is_visible",
            "author",
            "comments",
        ]

    created_at = serializers.BooleanField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=BlogUser.objects.all())
    comments = CommentSerializer(many=True, read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "text", "created_at"]

    user = serializers.PrimaryKeyRelatedField(queryset=BlogUser.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
