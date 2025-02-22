from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(
        'profile image', upload_to='users/profile', blank=True
    )
    short_description = models.TextField("short description", blank=True)

    like_posts = models.ManyToManyField(
        "posts.Post",
        verbose_name='list of likes-clicked posts',
        related_name="like_users",
        blank=True
    )

    following = models.ManyToManyField(
        "self",
        verbose_name='followed users',
        related_name="followers",
        symmetrical=False,
        through="users.Relationship"
    )

    def __str__(self):
        return self.username


class Relationship(models.Model):
    from_user = models.ForeignKey(
        "users.User",
        verbose_name="user who request follow",
        related_name="following_relationships",
        on_delete=models.CASCADE,
    )

    to_user = models.ForeignKey(
        "users.User",
        verbose_name="target of follow request",
        related_name="follower_relationships",
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"relation ({self.from_user} - {self.to_user})"
