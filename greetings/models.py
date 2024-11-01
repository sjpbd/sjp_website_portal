# greetings/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class Greeting(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='greetings')
    greeting_type = models.CharField(max_length=20, choices=[
        ('birthday', _('Birthday')),
        ('first_profession', _('First Profession')),
        ('final_profession', _('Final Profession')),
    ])
    date = models.DateField(db_index=True)
    message = models.TextField()
    is_sent = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'greeting_type', 'date']),
        ]

    def __str__(self):
        return f"{self.get_greeting_type_display()} greeting for {self.user.username}"

class UserPreference(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='greeting_preferences')
    receive_emails = models.BooleanField(default=True)
    receive_public_greetings = models.BooleanField(default=True)