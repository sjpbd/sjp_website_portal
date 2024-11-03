# home/admin.py

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from .models import About, Slide, DetailedAbout, Saint, SaintDetail, Member, NewsItem, FAQ, Obituary, GlobalSettings


@admin.register(About)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20})},
    }

    def has_add_permission(self, request):
        # Check if there's already an instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

# Your existing SlideAdmin registration here
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    readonly_fields = ('preview_image',)
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'preview_image', 'order', 'is_active')
        }),
    )

    def thumbnail(self, obj):
        return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
    thumbnail.short_description = 'Thumbnail'

    def preview_image(self, obj):
        return format_html('<img src="{}" width="300" height="200" style="object-fit: cover;" />', obj.image.url)
    preview_image.short_description = 'Image Preview'

    class Media:
        css = {
            'all': ('home/admin/css/thumbnail.css',)
        }


@admin.register(DetailedAbout)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Images', {
            'fields': ('detailed_image1', 'detailed_image2', 'detailed_image3')
        }),
        ('Content', {
            'fields': ('detailed_content1', 'detailed_content2', 'detailed_content3', 'detailed_content4', 'detailed_content5')
        }),
    )



class SaintDetailInline(admin.StackedInline):
    model = SaintDetail

@admin.register(Saint)
class SaintAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')
    inlines = [SaintDetailInline]

@admin.register(SaintDetail)
class SaintDetailAdmin(admin.ModelAdmin):
    list_display = ('saint',)




# @admin.register(Member)
# class MemberAdmin(admin.ModelAdmin):
#     list_display = ('name', 'order')
#     list_editable = ('order',)
#     search_fields = ('name',)


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('name_prefix', 'name_suffix', 'items_per_page')
    
    def has_add_permission(self, request):
        # Prevent creating multiple instances
        return not GlobalSettings.objects.exists()

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'full_name', 'first_name', 'middle_name', 'last_name', 'order')
    list_editable = ('order',)
    search_fields = ('first_name', 'middle_name', 'last_name')
    list_filter = ('created_at', 'updated_at')
    ordering = ('order', 'first_name', 'last_name')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'




@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'featured', 'created_at')
    list_filter = ('date', 'created_at', 'featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question', 'answer')



@admin.register(Obituary)
class ObituaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'death_date')
    list_filter = ('death_date',)
    search_fields = ('name',)

# constitution
from .models import Chapter

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

#photo album
from .models import Album, Photo

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'modified', 'is_visible')
    list_filter = ('is_visible', 'created', 'modified')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created', 'modified')
    list_filter = ('album', 'created', 'modified')
    search_fields = ('title', 'description', 'album__title')
    prepopulated_fields = {'slug': ('title',)}



from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ('name', 'title')

