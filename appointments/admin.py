# appointments/admin.py
from django.contrib import admin
from .models import AppointmentLetter, Notification

@admin.register(AppointmentLetter)
class AppointmentLetterAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'user', 'title', 'status', 'created_date')
    list_filter = ('status', 'created_date')
    search_fields = ('reference_number', 'user__email', 'title')
    ordering = ('-created_date',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment_letter', 'created_date', 'is_read')
    list_filter = ('is_read', 'created_date')
    search_fields = ('user__email',)
