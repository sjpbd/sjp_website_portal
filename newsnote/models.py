# newsnote/models.py

from django.db import models
from django.urls import reverse
from django.utils import timezone

class NewsNote(models.Model):
    title = models.CharField(max_length=200)
    issue = models.CharField(max_length=50)
    published_date = models.DateField()
    pdf_file = models.FileField(upload_to='newsnotes/')
    created_at = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"{self.title} - Issue: {self.issue}"

    def get_absolute_url(self):
        return reverse('newsnote_detail', kwargs={'pk': self.pk})