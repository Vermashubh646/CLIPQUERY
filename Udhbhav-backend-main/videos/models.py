from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models

class Video(models.Model):
    owner = models.ForeignKey(User ,default = 1, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField(null= True,blank= True)
    created_at = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)


    def __str__(self):
        return self.title
