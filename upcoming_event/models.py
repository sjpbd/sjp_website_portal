# upcoming_event/models.py
from django.db import models
from django.conf import settings
from users.models import CustomUser

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['event_date']


class Reminder(models.Model):
    event = models.ForeignKey(Event, related_name='reminders', on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.event.title} at {self.reminder_time}"
