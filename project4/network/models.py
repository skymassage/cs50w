from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True)
    followers = models.ManyToManyField("self", blank=True)

    def following_num(self):
        return self.following.all().count()

    def follower_num(self):
        return self.followers.all().count()

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def like_num(self):
        return self.likes.all().count()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "author": self.author.username,
            "post": self.message,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
