from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import IsOwnerPost
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


class NewLimitPageNumberPagination(PageNumberPagination):
    page_size = 5


class PostsV2(ModelViewSet):
    queryset = Post.objects.prefetch_related("comments").all()
    serializer_class = PostSerializer
    pagination_clas = NewLimitPageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        author_id = self.request.query_params.get("author", None)

        if author_id and author_id.isnumeric():
            queryset = queryset.filter(author=author_id)

            return queryset

        return queryset

    def create(self, request, *args, **kwargs):
        blogUser = BlogUser.objects.filter(user=request.user.id).first()
        request.data["author"] = blogUser.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_object(self):
        pk = self.kwargs.get("pk", "")

        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsOwnerPost(),
            ]
        return super().get_permissions()


####################    V2    ####################
####################    V2    ####################
