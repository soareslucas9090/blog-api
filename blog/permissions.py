from rest_framework import permissions


class IsOwnerPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user
