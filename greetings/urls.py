# greetings/urls.py
from django.urls import path
from .views import GreetingListView

app_name = 'greetings'

urlpatterns = [
    path('', GreetingListView.as_view(), name='greeting_list'),
]
