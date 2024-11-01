from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Institution(models.Model):
    # Basic Fields (Common for all institutions)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='institutions')
    establishment_year = models.PositiveIntegerField()
    short_history = models.TextField()

    # Fields for regular institutions
    ownership = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Type of ownership (e.g., Private, Government)"
    )
    administration = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Administrative body responsible for the institution"
    )
    grades = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Grade levels offered (e.g., I-X, XI-XII)"
    )
    students = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Total number of students"
    )
    teachers = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Total number of teachers"
    )
    office_staff = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Number of office staff members"
    )
    employees = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Total number of other employees"
    )
    status = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Current status of the institution"
    )

    # Fields specific to formation houses
    number_of_formees = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Number of formees in the formation house"
    )
    number_of_directors = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Number of formation directors"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('institutions:institution_detail', kwargs={'slug': self.slug})

    @property
    def is_formation_house(self):
        return self.category.name.lower() == 'formation house'

    class Meta:
        ordering = ['name']
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

class InstitutionImage(models.Model):
    institution = models.ForeignKey(
        Institution, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to='institution_images/',
        help_text="Upload an image for the institution"
    )
    caption = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Optional caption for the image"
    )

    def __str__(self):
        return f"Image for {self.institution.name}"

    class Meta:
        verbose_name = "Institution Image"
        verbose_name_plural = "Institution Images"