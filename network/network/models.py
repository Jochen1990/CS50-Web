from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="author")
    content = models.CharField(max_length=300)
    timestamp = models.DateTimeField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} : {self.content} : {self.timestamp} : {self.likes}"
    
    def serialize(self):
        return {
            "likes":self.likes
        }

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="user_followers")
    followers = models.IntegerField(default= 0)
    following = models.IntegerField(default= 0)

    def __str__(self):
        return f"{self.user} : {self.followers} : {self.following}"
    
class Follow_Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="user_following")
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="user_followed")

    def __str__(self):
        return f"{self.user} : {self.user_following}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likeduser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likedpost")