from rest_framework import serializers

from .models import *


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ["id", "name", "description", "is_author", "email"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at"]

    user = serializers.PrimaryKeyRelatedField(queryset=BlogUser.objects.all())
    created_at = serializers.DateTimeField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "tittle",
            "content",
            "created_at",
            "updated_at",
            "is_visible",
            "is_active",
            "author",
            "comments",
        ]

    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=BlogUser.objects.all())
    comments = CommentSerializer(many=True, read_only=True)

    def validate_tittle(self, value):
        tittle = value

        if len(tittle) < 5:
            raise serializers.ValidationError("Must have at least 5 chars.")

        return tittle

    def validate(self, aux):
        is_visible = aux.get("is_visible")
        is_active = aux.get("is_active")

        if is_visible and not is_active:
            raise serializers.ValidationError(
                {
                    "is_visible": "The is_visible field cannot be true while the is_active field is false."
                }
            )

        return super().validate(aux)
