# map_app/admin.py
from django.contrib import admin
from .models import Search, Ministry

admin.site.register(Search)
admin.site.register(Ministry)

