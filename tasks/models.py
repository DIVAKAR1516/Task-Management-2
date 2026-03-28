from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TaskUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passkey = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'title']

    def __str__(self):
        return self.title