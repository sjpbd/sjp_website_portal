# ministry/admin.py
from django.contrib import admin
from .models import Ministry, MinistryType
from django.db import models
from tinymce.widgets import TinyMCE

@admin.register(MinistryType)
class MinistryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'established_year')
    list_filter = ('type', 'established_year')
    search_fields = ('name', 'location', 'description')
    ordering = ('name', 'established_year')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }





