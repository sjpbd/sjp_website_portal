# greetings/admin.py
from django.contrib import admin
from .models import Greeting, UserPreference

@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('user', 'greeting_type', 'date', 'is_sent')
    list_filter = ('greeting_type', 'is_sent', 'date')
    search_fields = ('user__username', 'user__email', 'message')
    date_hierarchy = 'date'
    list_select_related = ('user',)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_emails', 'receive_public_greetings')
    list_filter = ('receive_emails', 'receive_public_greetings')
    search_fields = ('user__username', 'user__email')