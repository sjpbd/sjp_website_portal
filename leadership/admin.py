# admin.py
from django.contrib import admin
from .models import ProvinceLeadership, GeneralLeadership

@admin.register(ProvinceLeadership)
class ProvinceLeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email')
    search_fields = ('name', 'role')

@admin.register(GeneralLeadership)
class GeneralLeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email')
    search_fields = ('name', 'role')