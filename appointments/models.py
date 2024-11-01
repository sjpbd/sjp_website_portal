# appointments/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField
from django.urls import reverse

class AppointmentLetter(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('accepted', 'Accepted')
    )
    APPOINTMENT_TYPE_CHOICES = (
        ('new_appointment', 'New Appointment'),
        ('transfer', 'Transfer'),
        ('promotion', 'Promotion'),
        ('extension', 'Extension'),
    )
    # Basic Fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointment_letters')
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES)
    reference_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    
    # Dates
    created_date = models.DateTimeField(default=timezone.now)
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # For temporary appointments
    sent_date = models.DateTimeField(null=True, blank=True)
    
    # Letter Content
    header_image = models.ImageField(upload_to='appointment_headers/', null=True, blank=True)
    salutation = models.CharField(max_length=100)
    body_text = HTMLField()
    
    # Ministry Details
    previous_ministry = models.CharField(max_length=100, blank=True)
    new_ministry = models.CharField(max_length=100)
    new_designation = models.CharField(max_length=100)
    ministry_location = models.CharField(max_length=255)
    
    # Authority Details
    signature = models.ImageField(upload_to='signatures/')
    provincial_name = models.CharField(max_length=255)
    provincial_designation = models.CharField(max_length=255)
    footer_text = models.TextField()
    
    # Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_appointments'
    )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"Appointment Letter - {self.user.get_full_name()} - {self.reference_number}"

    def get_absolute_url(self):
        return reverse('appointments:letter_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # If this is a new appointment, automatically set previous_ministry
        if not self.pk and not self.previous_ministry:
            self.previous_ministry = self.user.current_ministry
        super().save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointment_notifications')
    appointment_letter = models.ForeignKey(AppointmentLetter, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_date']
        
    def __str__(self):
        return f"Notification for {self.user.get_full_name()} - {self.appointment_letter.reference_number}"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_date = timezone.now()
        self.save()

class AppointmentAcknowledgment(models.Model):
    appointment_letter = models.OneToOneField(AppointmentLetter, on_delete=models.CASCADE)
    acknowledged_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField()
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"Acknowledgment for {self.appointment_letter.reference_number}"
