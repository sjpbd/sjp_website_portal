# ministry/views.py
from django.views.generic import ListView
import django_tables2 as tables
from django_tables2 import SingleTableMixin
from .models import Ministry, MinistryType

class MinistryTable(tables.Table):
    class Meta:
        model = Ministry
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'type', 'location', 'established_year', 'description')

class MinistryListView(SingleTableMixin, ListView):
    model = Ministry
    table_class = MinistryTable
    template_name = 'ministry/ministry_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        ministry_type = self.request.GET.get('ministry_type')
        if ministry_type and ministry_type != 'all':
            queryset = queryset.filter(type__slug=ministry_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ministry_types'] = MinistryType.objects.all()
        context['ministry_table'] = self.get_table()
        return context
