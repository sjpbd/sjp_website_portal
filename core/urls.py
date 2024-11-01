"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

admin.site.site_header = "St. Joseph Province"
admin.site.site_title = "SJP Admin Portal"
admin.site.index_title = "Welcome to St. Joseph Province Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leadership/', include('leadership.urls', namespace='leadership')),
    path('users/', include('users.urls', namespace='users')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('greetings/', include('greetings.urls', namespace='greetings')),
    path('quotation/', include('quotation.urls', namespace='quotation')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('events/', include('upcoming_event.urls', namespace='upcoming_event')),
    path('announcement/', include('announcement.urls', namespace='announcement')),
    path('institutions/', include('institutions.urls', namespace='institutions')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('newsnote/', include('newsnote.urls', namespace='newsnote')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('ministry/', include('ministry.urls', namespace='ministry_app')),
    path('map_app/', include('map_app.urls', namespace='map_app')),
    path('', include('home.urls', namespace='home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

