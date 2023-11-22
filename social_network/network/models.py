from django.contrib.auth.models import AbstractUser
from django.db import models

# Database for social network app
class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=1000)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "poster: " + self.poster.username + "," \
                "content: " + self.content + "," \
                "date: " + str(self.date) + "," \

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "commenter: " + self.commenter.username + "," \
                "content: " + self.content + "," \
                "post: " + self.post.content + "," \
                "date: " + str(self.date)

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "liker: " + self.liker.username + "," \
                "post: " + self.post.content + "," \
                "date: " + str(self.date)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "follower: " + self.follower.username + "," \
                "followed: " + self.followed.username + "," \
                "date: " + str(self.date)


