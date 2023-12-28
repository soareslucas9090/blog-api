from django.urls import include, path

from .views import *

urlpatterns = [
    path("v1/posts/", posts, name="posts"),
    path("v1/posts/<int:pk>", post, name="post"),
    path("v2/posts/", PostsV2List.as_view(), name="posts"),
    path("v2/posts/<int:pk>", PostsV2Datails.as_view(), name="post"),
]
