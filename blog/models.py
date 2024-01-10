from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models


class Base(models.Model):
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(
        self,
        name,
        description,
        email,
        password=None,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            name=name,
            description=description,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        name,
        description,
        email,
        password,
    ):
        user = self.create_user(
            name=name,
            description=description,
            email=self.normalize_email(email),
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(verbose_name="name", max_length=255, null=False)
    email = models.EmailField(verbose_name="email", unique=True, null=False)
    description = models.TextField(verbose_name="description")
    is_author = models.BooleanField(verbose_name="is_author", null=False, default=False)

    date_joined = models.DateTimeField(verbose_name="data joined", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "name",
        "description",
    ]

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        str = f"{self.email}"
        return str

    class Meta:
        verbose_name = "USER"
        verbose_name_plural = "USERS"


class Post(Base):
    tittle = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_visible = models.BooleanField(null=False, default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        str = f"{self.tittle}"
        return str


class Comment(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        str = f"Coment of {self.user} on post {self.post}"
        return str
