from django import forms
from .models import Profile, ReligiousInfo, AcademicRecord, Experience, Publication, SocialLink

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 
                  'place_of_birth', 'mobile_number', 'email_address', 'father_name', 
                  'mother_name', 'parish_name', 'village_name', 'dist_name', 'blood_group', 
                  'passport_number', 'nid_number', 'title']

class ReligiousInfoForm(forms.ModelForm):
    class Meta:
        model = ReligiousInfo
        fields = ['date_of_joining', 'date_of_first_vows', 'date_of_final_vows']

class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ['degree', 'institution', 'grade', 'year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['position', 'organization', 'start_date', 'end_date']

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'authors', 'journal', 'year', 'doi']

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
