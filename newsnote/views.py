# newsnote/views.py
from django.views.generic import ListView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import NewsNote

class NewsNoteListView(ListView):
    model = NewsNote
    template_name = 'newsnote/newsnote_list.html'
    context_object_name = 'newsnotes'
    paginate_by = 12

    def get_queryset(self):
        queryset = NewsNote.objects.all()
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort_by', '-published_date')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(issue__icontains=search_query)
            )

        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort_by', '-published_date')
        return context

class NewsNoteDetailView(DetailView):
    model = NewsNote
    template_name = 'newsnote/newsnote_detail.html'
    context_object_name = 'newsnote'