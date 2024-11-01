from django.urls import path
from .views import news_feed, post_news, update_news, delete_news

app_name = 'announcement'

urlpatterns = [
    path('announcement_feed/', news_feed, name='announcement_feed'),
    path('post/', post_news, name='post_announcement'),
    path('update/<int:pk>/', update_news, name='update_news'),
    path('delete/<int:pk>/', delete_news, name='delete_news'),
]
