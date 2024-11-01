# ministry/urls.py
from django.urls import path
from .views import MinistryListView

app_name = 'ministry'

urlpatterns = [
    path('', MinistryListView.as_view(), name='ministry_list'),
]
