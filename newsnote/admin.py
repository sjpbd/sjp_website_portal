# newsnote/admin.py
from django.contrib import admin
from .models import NewsNote

@admin.register(NewsNote)
class NewsNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue', 'published_date', 'created_at')
    list_filter = ('published_date', 'created_at')
    search_fields = ('title', 'issue')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)