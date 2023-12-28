from django.urls import include, path

from .views import *

urlpatterns = [
    path("posts/", posts, name="posts"),
    path("posts/<int:pk>", post, name="post"),
]
