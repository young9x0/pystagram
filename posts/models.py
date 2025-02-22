from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="writer",
        on_delete=models.CASCADE
    )
    content = models.TextField("content")
    created = models.DateTimeField("created_date", auto_now_add=True)
    tags = models.ManyToManyField("posts.HashTag", verbose_name="hashtag list", blank=True)

    def __str__(self):
        return f"{self.user.username}'s post(id: {self.id})"


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name="post",
        on_delete=models.CASCADE,
    )
    photo = models.ImageField("photo", upload_to="post")


class Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="writer",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        verbose_name="post",
        on_delete=models.CASCADE,
    )
    content = models.TextField("content")
    created = models.DateTimeField("created_date", auto_now_add=True)


class HashTag(models.Model):
    name = models.CharField("tag name", max_length=50)

    def __str__(self):
        return self.name
