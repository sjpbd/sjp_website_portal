from .models import NewsPost

def latest_news(request):
    news_posts = NewsPost.objects.order_by('-created_at')[:10]
    return {'news_posts': news_posts}
