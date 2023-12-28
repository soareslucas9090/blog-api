from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


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
