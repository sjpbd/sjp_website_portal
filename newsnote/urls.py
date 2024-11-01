# newsnote/urls.py

from django.urls import path
from .views import NewsNoteListView, NewsNoteDetailView

app_name = 'newsnote'  # Set the app name for namespacing

urlpatterns = [
    path('', NewsNoteListView.as_view(), name='list'),  # URL for the NewsNote list view
    path('<int:pk>/', NewsNoteDetailView.as_view(), name='detail'),  # URL for the NewsNote detail view
]
