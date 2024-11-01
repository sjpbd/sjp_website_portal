# ministry/models.py
from django.db import models
from tinymce.models import HTMLField

class MinistryType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Ministry(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(MinistryType, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    established_year = models.IntegerField()
    description = HTMLField()

    def __str__(self):
        return self.name