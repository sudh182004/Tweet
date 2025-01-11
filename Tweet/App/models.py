from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tweets")
    content  = models.CharField(max_length=50)
    created_at  = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    @property
    def like_count(self):
        return self.likes.count()  

    @property
    def comment_count(self):
        return self.comments.count()  

class Comments(models.Model):
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=10) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} on {self.tweet.id}: {self.content[:50]}"

class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} liked Tweet {self.tweet.id}"