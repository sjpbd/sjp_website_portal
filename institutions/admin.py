from django.contrib import admin
from .models import Category, Institution, InstitutionImage

class InstitutionImageInline(admin.TabularInline):
    model = InstitutionImage
    extra = 1
    fields = ('image', 'caption')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'institution_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def institution_count(self, obj):
        return obj.institutions.count()
    institution_count.short_description = 'Number of Institutions'

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'establishment_year', 'get_institution_type_display')
    list_filter = ('category', 'status', 'establishment_year')
    search_fields = ('name', 'short_history')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [InstitutionImageInline]

    def get_fieldsets(self, request, obj=None):
        # Get the category from the existing object or from the request
        category = obj.category if obj else None
        if request.method == "POST":
            category_id = request.POST.get('category')
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    pass

        # Check if this is a formation house
        is_formation = category and category.name.lower() == 'formation house'

        if is_formation:
            return (
                (None, {
                    'fields': ('name', 'slug', 'category', 'short_history')
                }),
                ('Formation House Details', {
                    'fields': (
                        'establishment_year',
                        'number_of_formees',
                        'number_of_directors'
                    ),
                    'description': 'Information specific to formation houses'
                }),
            )
        else:
            return (
                (None, {
                    'fields': ('name', 'slug', 'category', 'short_history')
                }),
                ('Institution Details', {
                    'fields': (
                        'establishment_year',
                        'ownership',
                        'administration',
                        'grades',
                        'status'
                    ),
                    'description': 'Basic information about the institution'
                }),
                ('Statistics', {
                    'fields': (
                        'students',
                        'teachers',
                        'office_staff',
                        'employees'
                    ),
                    'description': 'Statistical information about the institution'
                }),
            )

    def get_institution_type_display(self, obj):
        return "Formation House" if obj.is_formation_house else "Regular Institution"
    get_institution_type_display.short_description = "Type"

    def get_list_display(self, request):
        """
        Customize list_display based on whether viewing formation houses or regular institutions
        """
        if request.GET.get('category__name__iexact') == 'formation house':
            return ('name', 'establishment_year', 'number_of_formees', 'number_of_directors')
        return ('name', 'category', 'establishment_year', 'students', 'status')

    class Media:
        js = ('admin/js/institution_admin.js',)

# Customize admin site
admin.site.site_header = "Holy Cross Institutions Admin"
admin.site.site_title = "Holy Cross Institutions Admin Portal"
admin.site.index_title = "Welcome to Holy Cross Institutions Admin Portal"