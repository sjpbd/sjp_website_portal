# upcoming_event/admin.py
from django.contrib import admin
from .models import Event, Reminder

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'creator')
    search_fields = ('title',)

class ReminderAdmin(admin.ModelAdmin):
    list_display = ('event', 'reminder_time')
    search_fields = ('event__title',)

admin.site.register(Event, EventAdmin)
admin.site.register(Reminder, ReminderAdmin)
