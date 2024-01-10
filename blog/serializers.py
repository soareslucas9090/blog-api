from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
            "last_login": {"write_only": True},
            "is_admin": {"write_only": True},
            "is_active": {"write_only": True},
            "is_superuser": {"write_only": True},
        }

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password


class User2AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at"]

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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
        read_only_fields = ["author"]

    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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
