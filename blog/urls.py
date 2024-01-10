from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

blog_router = SimpleRouter()
blog_router.register("posts", PostsV2)
blog_router.register("users", Users)

urlpatterns = [
    path("v1/posts/", posts, name="posts"),
    path("v1/posts/<int:pk>", post, name="post"),
    path("v2/", include(blog_router.urls)),
]
