# users/signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals
from .models import CustomUser

def send_approval_email(sender, instance, **kwargs):
    """
    Send approval email when user is approved by admin.
    This function handles the actual email sending logic.
    """
    subject = 'Your Profile Has Been Approved!'
    message = (
        f"Dear Br. {instance.get_full_name()},\n\n"
        "I am pleased to inform you that your profile has been approved. "
        "You can now log in to the St. Joseph Portal and start exploring all the features available to you.\n\n"
        "Thank you for being a part of this wonderful creation!\n\n"
        "Best regards,\n"
        "Br. Racy Daniel Godino, CSC\n"
        "Developer\n"
        "St. Joseph Website & Portal"
    )
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

@receiver(signals.pre_save, sender=CustomUser)
def handle_user_approval(sender, instance, **kwargs):
    """
    Signal handler to detect when a user is approved and send email.
    Checks if this is an existing user being approved for the first time.
    """
    try:
        # Get the user's previous state
        if instance.pk:  # Only for existing users
            previous = CustomUser.objects.get(pk=instance.pk)
            # Check if user is being approved for the first time
            if not previous.is_approved and instance.is_approved:
                send_approval_email(sender, instance)
    except CustomUser.DoesNotExist:
        pass  # This is a new user, no email needed