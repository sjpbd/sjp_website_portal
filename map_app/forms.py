# forms.py
from django import forms
from .models import Search, Ministry

class SearchForm(forms.ModelForm):
    address = forms.CharField(label='')

    class Meta:
        model = Search
        fields = ['address']

class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = ['name', 'ministry_type', 'address', 'latitude', 'longitude', 'description']
