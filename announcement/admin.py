from django.contrib import admin
from .models import NewsPost

class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Display title, author, and creation date in the list view
    list_filter = ('created_at', 'author')  # Add filters for the creation date and author
    search_fields = ('title', 'content')  # Enable search functionality by title and content
    ordering = ('-created_at',)  # Default ordering by creation date (newest first)
    date_hierarchy = 'created_at'  # Enable date hierarchy for easy navigation
    prepopulated_fields = {'title': ('content',)}  # Prepopulate title from content (if desired)

    # Customizing form layout for better usability
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author'),
        }),
        # Removed created_at from the fieldsets
    )
    
    # Make the author field read-only in admin to prevent manual changes
    def save_model(self, request, obj, form, change):
        if not change:  # Only set the author on creation
            obj.author = request.user
        super().save_model(request, obj, form, change)

# Register the model with the admin interface
admin.site.register(NewsPost, NewsPostAdmin)
