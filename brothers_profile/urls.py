from django.urls import path
from users.views import ProfileDetailView

app_name = 'brothers_profile'

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    # Add other URL patterns as needed
]




# from django.contrib.auth import views as auth_views
# from django.urls import path
# from users.views import ProfileDetailView
# from .views import (
#     CustomLoginView, profile_create_view, profile_view, 
#     update_profile, add_academic_record, add_experience, 
#     add_publication, update_social_links, export_to_pdf, clear_academic_records, search_view, profile_details,
# )

# app_name = 'brothers_profile'

# urlpatterns = [
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, next_page='/'), name='login'),
#     path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
#     path('profile/create/', profile_create_view, name='profile_create'),
#     path('profile/', profile_view, name='profile_view'),
#     path('profile/update/', update_profile, name='profile_update'),
#     path('academic/add/', add_academic_record, name='add_academic_record'),
#     path('experience/add/', add_experience, name='add_experience'),
#     path('publication/add/', add_publication, name='add_publication'),
#     path('social/update/', update_social_links, name='update_social_links'),
#     path('export/pdf/', export_to_pdf, name='export_to_pdf'),
#     path('academic/clear/', clear_academic_records, name='clear_academic_records'),
#     path('search/', search_view, name='search'),
#     path('profile-details/<int:user_id>/', profile_details, name='profile_details'),
#     path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
# ]

