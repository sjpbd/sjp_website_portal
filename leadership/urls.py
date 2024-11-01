# leadership/urls.py
from django.urls import path
from . import views

app_name = 'leadership'

urlpatterns = [
    path('<str:leadership_type>/', views.leadership_view, name='leadership'),
    path('province/', views.province_leadership_view, name='province_leadership'),
    path('general/', views.general_leadership_view, name='general_leadership'),
]
