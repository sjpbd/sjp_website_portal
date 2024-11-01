from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView 
from .views import brothers_contacts
from .views import MainPageView
from .views import delete_academic_info, delete_apostolic_info

app_name = 'users' 

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('signup/', views.signup, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('under-review/', views.under_review, name='under_review'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('academic/add/', views.add_academic_info, name='add_academic_info'),
    path('apostolic/add/', views.add_apostolic_info, name='add_apostolic_info'),
    path('academic/edit/<int:pk>/', views.edit_academic_info, name='edit_academic_info'),  # Display form
    path('academic-info/delete/<int:pk>/', delete_academic_info, name='delete_academic_info'),
    path('academic/update/<int:pk>/', views.edit_academic_info, name='update_academic_info'),  # Handle update
    path('apostolic/edit/<int:pk>/', views.edit_apostolic_info, name='edit_apostolic_info'),
    path('apostolic-info/<int:pk>/delete/', delete_apostolic_info, name='delete_apostolic_info'),
    path('apostolic/update/<int:pk>/', views.update_apostolic_info, name='update_apostolic_info'),
    path('profile/upload_picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('brothers-contacts/', brothers_contacts, name='brothers_contacts'),
]
