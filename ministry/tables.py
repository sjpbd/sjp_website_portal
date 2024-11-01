# ministry/tables.py
import django_tables2 as tables
from .models import Ministry

class MinistryTable(tables.Table):
    class Meta:
        model = Ministry
        template_name = 'django_tables2/bootstrap4.html'  # Use Bootstrap 4 styling

        fields = ('name', 'type__name', 'location', 'established_year', 'description')
        attrs = {'class': 'table table-striped table-bordered'}
