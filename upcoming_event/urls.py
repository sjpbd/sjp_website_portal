# upcoming_event/urls.py
from django.urls import path
from . import views

app_name = 'upcoming_event'

urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    # path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/', views.event_list, name='event_list'),  # Define event_list URL pattern
]
