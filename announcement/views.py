from django.shortcuts import render, redirect, get_object_or_404
from .models import NewsPost
from .forms import NewsPostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import user_must_be_approved
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@user_must_be_approved
def news_feed(request):
    # Get all news posts ordered by creation date
    news_list = NewsPost.objects.all().order_by('-created_at')
    
    # Number of posts per page
    posts_per_page = 5
    
    # Create paginator object
    paginator = Paginator(news_list, posts_per_page)
    
    # Get page number from request
    page = request.GET.get('page', 1)
    
    try:
        news_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        news_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        news_posts = paginator.page(paginator.num_pages)
    
    return render(request, 'announcement/announcement_feed.html', {
        'news_posts': news_posts,
        'latest_news': NewsPost.objects.all().order_by('-created_at')[:5]  # For marquee
    })


# @user_must_be_approved
# def news_feed(request):
#     news_posts = NewsPost.objects.all().order_by('-created_at')
#     return render(request, 'announcement/announcement_feed.html', {'news_posts': news_posts})

@login_required
@user_must_be_approved
def post_news(request):
    if request.method == 'POST':
        form = NewsPostForm(request.POST)
        if form.is_valid():
            news_post = form.save(commit=False)
            news_post.author = request.user  # Link the post to the logged-in user
            news_post.save()
            messages.success(request, 'Your news post has been successfully created!')
            return redirect('announcement:announcement_feed')
    else:
        form = NewsPostForm()
    return render(request, 'announcement/post_announcement.html', {'form': form})

@login_required
@user_must_be_approved
def update_news(request, pk):
    news_post = get_object_or_404(NewsPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = NewsPostForm(request.POST, instance=news_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your news post has been successfully updated!')
            return redirect('announcement:announcement_feed')
    else:
        form = NewsPostForm(instance=news_post)
    return render(request, 'announcement/post_announcement.html', {'form': form})



@login_required
def delete_news(request, pk):
    news_post = get_object_or_404(NewsPost, pk=pk, author=request.user)
    
    if request.method == 'POST':
        news_post.delete()
        messages.success(request, 'Your news post has been successfully deleted!')
        return redirect('announcement:announcement_feed')
    
    # Render confirmation page on GET request
    return render(request, 'announcement/confirm_delete.html', {'news_post': news_post})


