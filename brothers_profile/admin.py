from django.contrib import admin
from .models import Profile, ReligiousInfo, AcademicRecord, Experience, Publication, SocialLink

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'title', 'profile_picture')
    search_fields = ('user__username', 'first_name', 'last_name')

@admin.register(ReligiousInfo)
class ReligiousInfoAdmin(admin.ModelAdmin):
    list_display = ('profile', 'date_of_joining', 'date_of_final_vows')

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('profile', 'degree', 'institution', 'year')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'position', 'organization', 'start_date', 'end_date')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'authors', 'year')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('profile', 'platform', 'url')
    

