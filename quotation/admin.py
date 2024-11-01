# admin.py
from django.contrib import admin
from .models import Quote, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'category', 'is_featured', 'display_count')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('text', 'author', 'source')
    readonly_fields = ('display_count', 'created_at', 'updated_at')
    actions = ['make_featured', 'remove_featured']

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected quotes as featured"

    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
    remove_featured.short_description = "Remove featured status from selected quotes"
