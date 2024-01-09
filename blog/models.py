from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        abstract = True


class BlogUser(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    is_author = models.BooleanField(null=False, default=False)
    email = models.EmailField(null=False, unique=True)

    def __str__(self):
        str = f"{self.name}"
        return str


class Post(Base):
    tittle = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_visible = models.BooleanField(null=False, default=True)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        str = f"{self.tittle}"
        return str


class Comment(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        str = f"Coment of {self.user} on post {self.post}"
        return str
