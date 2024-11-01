# map_app/urls.py
from django.urls import path
from .views import index

app_name = 'map_app'
urlpatterns = [
    path('', index, name='index'),
]
