# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe  # Import mark_safe
from .models import CustomUser, AcademicInformation, ApostolicInformation

class AcademicInformationInline(admin.TabularInline):
    model = AcademicInformation
    extra = 1
    verbose_name_plural = "Academic Information"

class ApostolicInformationInline(admin.TabularInline):
    model = ApostolicInformation
    extra = 1
    verbose_name_plural = "Apostolic Information"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['avatar', 'username', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'is_staff']
    list_filter = ['role', 'is_approved', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'middle_name', 'date_of_birth', 'blood_group', 'nid_number', 
                'passport_number', 'village', 'parish', 'diocese', 'mobile', 
                'current_ministry', 'designation', 'first_profession_date', 
                'final_profession_date', 'role', 'is_approved', 'profile_picture'
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'middle_name', 'date_of_birth', 'blood_group', 'nid_number', 
                'passport_number', 'village', 'parish', 'diocese', 'mobile', 
                'current_ministry', 'designation', 'first_profession_date', 
                'final_profession_date', 'role', 'is_approved', 'profile_picture'
            )
        }),
    )
    
    inlines = [AcademicInformationInline, ApostolicInformationInline]

    def avatar(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" style="width: 40px; height: 40px; border-radius: 50%;" />')
        return 'No Image'
    
    avatar.short_description = 'Avatar'  # Optional human-readable name for the avatar column

# Register the CustomUserAdmin with CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)


