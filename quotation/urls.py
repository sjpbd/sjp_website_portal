# urls.py
from django.urls import path
from .views import daily_inspiration
from .views import random_quote  # Ensure you import your API view
from .views import QuoteListView

app_name = 'quotation'

urlpatterns = [
    path('daily-inspiration/', daily_inspiration, name='daily_inspiration'),
    path('api/random-quote/', random_quote, name='random_quote'),  # existing API endpoint
    path('api/quotes/', QuoteListView.as_view(), name='quote-list'),
]