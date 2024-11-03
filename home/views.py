from django.shortcuts import render, get_object_or_404
from .models import Slide, About, DetailedAbout, Saint, Member, NewsItem, FAQ, Obituary, TeamMember,GlobalSettings
from django.http import JsonResponse
from newsnote.models import NewsNote
from django.views.decorators.http import require_GET
from django.urls import path
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def message(request):
    return render(request, 'home/message.html')

def home(request):
    slides = Slide.objects.all()
    about_us = About.objects.first()
    # news_items = NewsItem.objects.all()  # Fetch all news items
    news_items = NewsItem.objects.all()[:3]  # Get the latest 3 news items
    faqs = FAQ.objects.all()
    newsnotes = NewsNote.objects.all()
    context = {
        'slides': slides,
        'about_us': about_us,
        'news_items': news_items,
        'faqs': faqs,
        'newsnotes': newsnotes, 
    }
    return render(request, 'home/home.html', context)

def about(request):
    about_us = About.objects.first()
    return render(request, 'home/about.html', {'about_us': about_us})

def slider(request):
    slides = Slide.objects.all()
    return render(request, 'home/slider.html', {'slides': slides})



def members(request):
    # Get global settings
    settings = GlobalSettings.objects.first()
    items_per_page = settings.items_per_page if settings else 20
    
    # Get the selected letter and page number from query parameters
    selected_letter = request.GET.get('letter', 'all')
    page = request.GET.get('page', 1)
    
    # Base queryset
    members_list = Member.objects.all()
    
    # Get all unique first letters from member names (considering all name parts)
    all_members = members_list
    available_letters = set()
    for member in all_members:
        available_letters.add(member.first_name[0].upper())
        if member.middle_name:
            available_letters.add(member.middle_name[0].upper())
        available_letters.add(member.last_name[0].upper())
    available_letters = sorted(available_letters)
    
    # Filter members based on selected letter
    if selected_letter.lower() != 'all':
        members_list = members_list.filter(
            Q(first_name__istartswith=selected_letter) |
            Q(middle_name__istartswith=selected_letter) |
            Q(last_name__istartswith=selected_letter)
        )
    
    # Order the results
    members_list = members_list.order_by('order', 'first_name', 'last_name')
    
    # Paginate the results
    paginator = Paginator(members_list, items_per_page)
    try:
        members_page = paginator.page(page)
    except PageNotAnInteger:
        members_page = paginator.page(1)
    except EmptyPage:
        members_page = paginator.page(paginator.num_pages)
    
    context = {
        'members': members_page,
        'selected_letter': selected_letter,
        'available_letters': available_letters,
        'settings': settings,
        'total_members': members_list.count(),
    }
    
    return render(request, 'home/members.html', context)

def obituary_view(request):
    obituaries = Obituary.objects.all().order_by('death_date')
    return render(request, 'home/obituary.html', {'obituaries': obituaries})

def contact(request):
    return render(request, 'home/contact.html')

# def detailed_about(request):
#     detailed_about_obj = DetailedAbout.objects.first()
#     return render(request, 'home/detailed_about.html', {'detailed_about': detailed_about_obj})
def detailed_about(request):
    try:
        detailed_about_obj = DetailedAbout.objects.first()
    except DetailedAbout.DoesNotExist:
        detailed_about_obj = None
    
    if detailed_about_obj:
        context = {
            'detailed_about': detailed_about_obj
        }
        return render(request, 'home/detailed_about.html', context)
    else:
        # Handle case where detailed about us content is not found
        return render(request, 'home/detailed_about.html', {'detailed_about': None})

def detailed_holyones(request):
    saints_list = Saint.objects.all()
    return render(request, 'home/detailed_holyones.html', {'saints': saints_list})

def saint_detail_api(request, saint_id):
    saint = get_object_or_404(Saint, id=saint_id)
    data = {
        'name': saint.name,
        'designation': saint.designation,
        'image_url': saint.image.url if saint.image else '',
        'detail': {
            'full_content': saint.detail.full_content
        }
    }
    return JsonResponse(data)

@require_GET
def api_news_items(request):
    page = int(request.GET.get('page', 1))
    items_per_page = 3
    
    # Get all news items
    all_news = NewsItem.objects.all().order_by('-date')
    paginator = Paginator(all_news, items_per_page)
    
    try:
        news_page = paginator.page(page)
    except:
        return JsonResponse({'news_items': []})
    
    news_items = [{
        'title': item.title,
        'content': item.content[:200] + '...' if len(item.content) > 200 else item.content,
        'image_url': item.image.url if item.image else None,
        'date': item.date.strftime('%d %b %Y'),
        'slug': item.slug,
    } for item in news_page]
    
    return JsonResponse({
        'news_items': news_items,
        'has_next': news_page.has_next(),
        'has_previous': news_page.has_previous(),
        'total_pages': paginator.num_pages,
    })

def news_detail(request, slug):
    news_item = get_object_or_404(NewsItem, slug=slug)
    recent_news = NewsItem.objects.exclude(id=news_item.id)[:3]  # Exclude current news item and get latest 3
    context = {
        'news_item': news_item,
        'recent_news': recent_news,
    }
    return render(request, 'home/details_news.html', context)



def news_list(request):
    news_items = NewsItem.objects.all()
    context = {
        'news_items': news_items,
    }
    return render(request, 'home/news_list.html', context)


# Constitution
from .models import Chapter

def chapter_list(request):
    chapters = Chapter.objects.all()
    return render(request, 'home/chapter_list.html', {'chapters': chapters})

def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    chapters = Chapter.objects.all()  # Fetch all chapters for the navigation
    return render(request, 'home/chapter_detail.html', {'chapter': chapter, 'chapters': chapters})



# Photo Album
from django.views.generic import ListView, DetailView
from .models import Album, Photo

class AlbumListView(ListView):
    model = Album
    template_name = 'photos/album_list.html'
    context_object_name = 'albums'
    queryset = Album.objects.filter(is_visible=True)

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'photos/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        return context

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.object.album
        return context



def team_view(request):
    team_members = TeamMember.objects.all()
    return render(request, 'home/province_administration.html', {'team_members': team_members})