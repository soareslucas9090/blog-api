from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

blog_router = SimpleRouter()
blog_router.register("posts", PostsV2)
blog_router.register("users", Users)
blog_router.register("comments", Comments)
blog_router.register("tags", Tags)
blog_router.register("categorys", Categorys)

urlpatterns = [
    # path("v1/posts/", posts, name="posts"),
    # path("v1/posts/<int:pk>", post, name="post"),
    path("v2/", include(blog_router.urls)),
]
