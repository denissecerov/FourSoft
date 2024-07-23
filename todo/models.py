from django.db import models
from django.contrib.auth.models import User
import datetime

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255,default='Default Name')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Alarm(models.Model):
    time = models.TimeField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.time.strftime("%I:%M %p")
    
    