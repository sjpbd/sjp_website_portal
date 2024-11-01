# map_app/models.py
from django.db import models

class Search(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Ministry(models.Model):
    MINISTRY_TYPES = [
        ('SCH', 'School'),
        ('TSC', 'Technical School'),
        ('HST', 'Hostel'),
        ('RHB', 'Rehabilitation Center'),
        ('FRM', 'Formation House'),
        ('ASH', 'Ashram'),
        ('OTH', 'Other'),
    ]

    name = models.CharField(max_length=200)
    ministry_type = models.CharField(max_length=3, choices=MINISTRY_TYPES)
    address = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_ministry_type_display()})"
