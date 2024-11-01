from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate'),
    path('success/', views.payment_success, name='success'),
    path('fail/', views.payment_fail, name='fail'),
    path('cancel/', views.payment_cancel, name='cancel'),
]
