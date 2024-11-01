# appointments/urls.py
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('letters/', views.AppointmentLetterListView.as_view(), name='letter_list'),
    path('letters/create/', views.AppointmentLetterCreateView.as_view(), name='letter_create'),
    path('letters/<int:pk>/', views.AppointmentLetterDetailView.as_view(), name='letter_detail'),  # Fixed
    path('letters/<int:pk>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('letters/<int:pk>/send/', views.send_letter, name='send_letter'),
]
