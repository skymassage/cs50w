from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", blank=True, related_name="followers")

    def following_num(self):
        # For the "ManyToManyField" field in the model, 
        # use the ".all()" after the field attribute to access all objects of the field.
        return self.following.all().count()

    def follower_num(self):
        return self.followers.all().count()

    def post_num(self):
        return self.posts.all().count()

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    dislikes = models.ManyToManyField(User, blank=True, related_name="disliked_posts")

    def like_num(self):
        return self.likes.all().count()

    def dislike_num(self):
        return self.dislikes.all().count()

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