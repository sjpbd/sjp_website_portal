from django.urls import path
from . import views

app_name = 'institutions'

urlpatterns = [
    path('', views.overview, name='overview'),
    path('institution/<slug:slug>/', views.institution_detail, name='institution_detail'),
]
