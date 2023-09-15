from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# ---I WROTE THIS CODE---
# Model representing an application user
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    background_image = models.ImageField(null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing the status of an application user
class Status(models.Model):
    status = models.TextField(
        null=True, blank=True, default=None
    )  # Field to store long sentences
    created_at = models.DateTimeField(auto_now_add=True)
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing user posts in a gallery
class Gallery(models.Model):
    post_image = models.ImageField(null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing user followings
class Followings(models.Model):
    current_user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="followings_current_user"
    )
    following = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="followings_following"
    )

    class Meta:
        unique_together = ("current_user", "following")


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing chat messages
class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# ---END OF CODE THAT I WROTE---
