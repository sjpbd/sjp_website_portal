from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Institution

def overview(request):
    categories = Category.objects.all()
    all_institutions = Institution.objects.all().select_related('category')  # For sidebar
    filtered_institutions = all_institutions

    query = request.GET.get('q')
    if query:
        filtered_institutions = filtered_institutions.filter(
            Q(name__icontains=query) |
            Q(short_history__icontains=query)
        )

    category_filter = request.GET.get('category')
    if category_filter:
        filtered_institutions = filtered_institutions.filter(category__slug=category_filter)

    paginator = Paginator(filtered_institutions, 9)  # Show 9 institutions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'page_obj': page_obj,
        'query': query,
        'category_filter': category_filter,
        'institutions': all_institutions,  # For sidebar
    }
    return render(request, 'institutions/overview.html', context)

def institution_detail(request, slug):
    institution = get_object_or_404(Institution, slug=slug)
    context = {'institution': institution}
    return render(request, 'institutions/institution_detail.html', context)