# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from datetime import date

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    )
    
    middle_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    nid_number = models.CharField(max_length=20, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    village = models.CharField(max_length=100, blank=True)
    parish = models.CharField(max_length=100, blank=True)
    diocese = models.CharField(max_length=100, blank=True)
    mobile = PhoneNumberField(null=False, blank=False, unique=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    current_ministry = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    first_profession_date = models.DateField(null=True, blank=True)
    final_profession_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    is_approved = models.BooleanField(default=False)
    
    # Add profile picture field
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    # Property to calculate user's age dynamically
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return self.username

class AcademicInformation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='academic_info')
    degree_name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=200)
    passing_year = models.IntegerField()
    gpa = models.FloatField()

class ApostolicInformation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='apostolic_info')
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)  # to_date is now optional if still working
    designation = models.CharField(max_length=100)
    apostolate_name = models.CharField(max_length=200)
    is_current = models.BooleanField(default=False)  # New field to indicate if still working

    def __str__(self):
        return f"{self.apostolate_name} - {self.designation}"




