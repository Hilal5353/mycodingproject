from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
import random

def random_profile_pic():
    return random.choice(['profile1.png', 'profile3.png', 'profile4.png', 'profile5.png', 'profile6.png', 'profile7.png','profile2.png'])

User = get_user_model()

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, max_length=20)
    id_user = models.IntegerField()
    bio = models.TextField(max_length=200, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default=random_profile_pic)
    location = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField(upload_to='post_images')
    user = models.CharField(max_length=100)
    caption = models.TextField()
    crated_at = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)


    def __str__(self):
        return self.user


class PostReport(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)  # Optional reason user can write
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by.username} on post {self.post.id}"


class LikedPost(models.Model):
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    vote_type = models.CharField(max_length=5, choices=VOTE_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.vote_type}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    @property
    def profile_picture(self):
        return self.user.profile.profileimg  # Get the profile picture from the user's Profile model

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    @property
    def profile_picture(self):
        return self.user.profile.profileimg  # Get the profile picture from the user's Profile model

    def __str__(self):
        return f"Reply by {self.user.username} to {self.comment.id}"
    
class Followercount(models.Model):
    follower = models.CharField(max_length=100) 
    user = models.CharField(max_length=100)   

    def __str__(self):
        return self.user
