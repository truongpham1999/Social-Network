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
    
    def like_count(self):
        return self.likes.count()
    
    def is_like_by_user(self, user):
        return self.likes.filter(liker=user).exists()

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "commenter: " + self.commenter.username + "," \
                "content: " + self.content + "," \
                "post: " + self.post.content + "," \
                "date: " + str(self.date)
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "commenter": {
                "id": self.commenter.id,
                "username": self.commenter.username
            },
            "post": self.post.id,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
            }

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
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
