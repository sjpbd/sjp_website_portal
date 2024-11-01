# greetings/tasks.py
from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings
from django.utils import timezone
from .models import Greeting
from django.contrib.auth import get_user_model

@shared_task
def send_greetings():
    today = timezone.now().date()
    greetings = Greeting.objects.filter(date=today, is_sent=False).select_related('user')
    
    emails = []
    for greeting in greetings:
        if greeting.user.greeting_preferences.receive_emails:
            subject = f"{greeting.get_greeting_type_display()} Greetings for {greeting.user.get_full_name()}"
            message = greeting.message
            from_email = settings.DEFAULT_FROM_EMAIL
            
            if greeting.user.greeting_preferences.receive_public_greetings:
                recipient_list = get_user_model().objects.exclude(id=greeting.user.id).values_list('email', flat=True)
                emails.append((subject, message, from_email, recipient_list))
            
            # Send personal email to the user
            personal_subject = f"Happy {greeting.get_greeting_type_display()}!"
            personal_message = f"Dear {greeting.user.get_full_name()},\n\n{greeting.message}"
            emails.append((personal_subject, personal_message, from_email, [greeting.user.email]))
    
    send_mass_mail(emails, fail_silently=False)
    
    Greeting.objects.filter(id__in=[g.id for g in greetings]).update(is_sent=True)
