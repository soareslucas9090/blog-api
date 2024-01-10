from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import IsAdminUser, IsOwnerPost, IsOwnerUser
from .serializers import *

####################    V1    ####################
####################    V1    ####################


@api_view(http_method_names=["get", "post"])
def posts(request):
    if request.method == "GET":
        posts = Post.objects.prefetch_related("comments").all()
        serializer = PostSerializer(
            instance=posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["get", "patch", "delete"])
def post(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related("comments").all(), pk=pk)

    if request.method == "GET":
        serializer = PostSerializer(
            instance=post, many=False, context={"request": request}
        )
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = PostSerializer(
            instance=post,
            data=request.data,
            many=False,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


####################    V1    ####################
####################    V1    ####################

##################################################

####################    V2    ####################
####################    V2    ####################


class PostsPageNumberPagination(PageNumberPagination):
    page_size = 5


class PostsV2(ModelViewSet):
    queryset = Post.objects.prefetch_related("comments").all()
    serializer_class = PostSerializer
    pagination_class = PostsPageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    http_method_names = ["get", "options", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        author_id = self.request.query_params.get("author", None)

        if author_id and author_id.isnumeric():
            queryset = queryset.filter(author=author_id)

            return queryset

        return queryset

    def create(self, request, *args, **kwargs):
        print(request)
        user = User.objects.filter(pk=request.user.id).first()
        if user.is_author:
            request.data["author"] = user.id

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            dict = {"detail": "You need author permission."}
            return Response(dict, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsOwnerPost(),
            ]
        return super().get_permissions()


class Users(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PostsPageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    http_method_names = ["get", "options", "head", "patch", "delete", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password256 = make_password(password=request.data["password"])

        serializer.save(password=password256)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if "date_joined" in request.data:
            request.data.pop("date_joined")
        if "is_superuser" in request.data:
            request.data.pop("is_superuser")

        if not isinstance(request.user, AnonymousUser):
            if not request.user.is_admin:
                if "is_staff" in request.data:
                    request.data.pop("is_staff")
                if "is_admin" in request.data:
                    request.data.pop("is_admin")
                if "is_active" in request.data:
                    request.data.pop("is_active")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not isinstance(request.user, AnonymousUser):
            if request.user.is_admin:
                queryset = self.filter_queryset(self.get_queryset())

                page = self.paginate_queryset(queryset)
                self.serializer_class = User2AdminSerializer
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)

        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            if not isinstance(self.request.user, AnonymousUser):
                if not self.request.user.is_admin:
                    return [
                        IsOwnerUser(),
                    ]
                else:
                    return [
                        IsAdminUser(),
                    ]

        return super().get_permissions()


####################    V2    ####################
####################    V2    ####################
