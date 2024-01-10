from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsOwnerPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwnerUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, AnonymousUser)


class IsOwnerComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
