# models.py
from django.db import models

class BaseLeadership(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

class ProvinceLeadership(BaseLeadership):
    # Add any province-specific fields here
    pass

class GeneralLeadership(BaseLeadership):
    # Add any general-specific fields here
    pass