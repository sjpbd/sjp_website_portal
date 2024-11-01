from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile model that links to the CustomUser or default User model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='img/default_avatar_profile.jpg')
    profile_thumbnail = ImageSpecField(source='profile_picture',
                                       processors=[ResizeToFill(100, 100)],
                                       format='JPEG',
                                       options={'quality': 60})
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(max_length=50, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    parish_name = models.CharField(max_length=100, blank=True)
    village_name = models.CharField(max_length=100, blank=True)
    dist_name = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    nid_number = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=100, default="Religious Brother")

    def __str__(self):
        return self.user.username

# Model for religious information associated with a profile
class ReligiousInfo(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_of_joining = models.DateField(null=True, blank=True)
    date_of_first_vows = models.DateField(null=True, blank=True)
    date_of_final_vows = models.DateField(null=True, blank=True)

# Model for academic records linked to a profile
class AcademicRecord(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='academic_records')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    grade = models.CharField(max_length=20)
    year = models.IntegerField()

# Model for experience records linked to a profile
class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

# Model for publication records linked to a profile
class Publication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    journal = models.CharField(max_length=200)
    year = models.IntegerField()
    doi = models.CharField(max_length=100, blank=True)

# Model for social media links linked to a profile
class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50)
    url = models.URLField()

# Signal to create or update a profile automatically when a user is created or updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    # Ensure the profile is saved when the user object is updated
    instance.profile.save()
