# home/models.py

from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.core.paginator import Paginator
from django.utils import timezone


class Slide(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slider_images/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class About(models.Model):
    title = models.CharField(max_length=200, default="About Us")
    image = models.ImageField(upload_to='about_us/')
    content = HTMLField()

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title


class DetailedAbout(models.Model):
    title = models.CharField(max_length=200)
    detailed_image1 = models.ImageField(upload_to='about_images/')
    detailed_image2 = models.ImageField(upload_to='about_images/')
    detailed_image3 = models.ImageField(upload_to='about_images/')
    detailed_content1 = models.TextField()
    detailed_content2 = models.TextField()
    detailed_content3 = models.TextField()
    detailed_content4 = models.TextField()
    detailed_content5 = models.TextField()

    def __str__(self):
        return self.title


class Saint(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    short_description = models.TextField()
    image = models.ImageField(upload_to='saints/', null=True, blank=True)

    def __str__(self):
        return self.name

class SaintDetail(models.Model):
    saint = models.OneToOneField(Saint, on_delete=models.CASCADE, related_name='detail')
    full_content = models.TextField()

    def __str__(self):
        return f"Details for {self.saint.name}"




# class Member(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='members/')
#     order = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name



class GlobalSettings(models.Model):
    name_prefix = models.CharField(max_length=10, default="Br.", help_text="e.g., Br., Fr., Sr.")
    name_suffix = models.CharField(max_length=10, default="CSC", help_text="e.g., CSC")
    items_per_page = models.IntegerField(default=20, help_text="Number of members to show per page")

    class Meta:
        verbose_name = "Global Setting"
        verbose_name_plural = "Global Settings"

    def __str__(self):
        return f"Global Settings (Prefix: {self.name_prefix}, Suffix: {self.name_suffix})"

    def save(self, *args, **kwargs):
        if not self.pk and GlobalSettings.objects.exists():
            return  # Ensure only one instance exists
        return super(GlobalSettings, self).save(*args, **kwargs)

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='members/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['order', 'first_name', 'last_name']
        
    @property
    def full_name(self):
        # Get global settings
        settings = GlobalSettings.objects.first()
        prefix = f"{settings.name_prefix} " if settings else "Br. "
        suffix = f" {settings.name_suffix}" if settings else " CSC"
        
        # Build full name
        name_parts = [self.first_name]
        if self.middle_name:
            name_parts.append(self.middle_name)
        name_parts.append(self.last_name)
        
        return f"{prefix}{' '.join(name_parts)}{suffix}"

    def __str__(self):
        return self.full_name




class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

    @classmethod
    def latest_news(cls, limit=3):
        return cls.objects.all()[:limit]

    
 


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = HTMLField('Content')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question



class Obituary(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    image = models.ImageField(upload_to='obituary_images/')

    class Meta:
        verbose_name_plural = "Obituaries"

    def __str__(self):
        return self.name

# constitution viewer

class Chapter(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()

    def __str__(self):
        return self.title

#photo Album
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024)
    thumb = ImageSpecField(source='cover_image',
                           processors=[ResizeToFill(300, 200)],
                           format='JPEG',
                           options={'quality': 90})
    cover_image = models.ImageField(upload_to='albums')
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:album_detail', args=[str(self.slug)])

class Photo(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='photos')
    thumb = ImageSpecField(source='image',
                           processors=[ResizeToFill(300, 200)],
                           format='JPEG',
                           options={'quality': 90})
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:photo_detail', args=[str(self.album.slug), str(self.slug)])




class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/counselors/')

    def __str__(self):
        return self.name