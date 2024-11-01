# announcement/models.py

from django.db import models
from django.conf import settings

class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the user

    def __str__(self):
        return self.title
