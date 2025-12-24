from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) #null and blank are temporary here -> remove them later!
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class Event(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location_name = models.CharField(max_length=255)  # Human-readable name
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%Y-%m-%d')})"


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participants")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # ensures one participation per user per event

    def __str__(self):
        return f"{self.user.username} joined {self.event.title}"

