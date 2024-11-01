# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, AcademicInformation, ApostolicInformation
from phonenumber_field.formfields import PhoneNumberField
from django_countries.widgets import CountrySelectWidget
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.contrib import messages

# Define blood group choices
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('Unknown', 'Unknown'),  # Optional, if you want to include an unknown option
]
# Define diocese choices
DIOCESE_CHOICES = [
    ('Dhaka', 'Archdiocese of Dhaka'),
    ('Chattogram', 'Archdiocese of Chattogram'),
    ('Rajshahi', 'Diocese of Rajshahi'),
    ('Khulna', 'Diocese of Khulna'),
    ('Dinajpur', 'Diocese of Dinajpur'),
    ('Mymensingh', 'Diocese of Mymensingh'),
    ('Sylhet', 'Diocese of Sylhet'),
    ('Barishal', 'Diocese of Barishal'),
]

class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField(required=False)

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        # Check if the file is empty
        if not profile_picture:
            raise ValidationError("No file uploaded. Please upload a profile picture.")

        # Validate file type
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        if not any(profile_picture.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError("Invalid file format. Please upload a JPEG, PNG, or GIF image.")

        # Validate file size (limit to 5MB)
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if profile_picture.size > max_size:
            raise ValidationError("File size too large. Please upload an image smaller than 5MB.")

        return profile_picture


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email', 'first_name', 'last_name', 'middle_name', 'date_of_birth',
            'blood_group', 'nid_number', 'passport_number', 'village',
            'parish', 'diocese', 'mobile', 'current_ministry', 'designation',
            'first_profession_date', 'final_profession_date', 'profile_picture',
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'first_profession_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'final_profession_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'current_ministry': forms.TextInput(attrs={'placeholder': 'Write the name of your Institution/House'}),
            'country': CountrySelectWidget(),
        }
        
    # Override __init__ to customize the blood_group field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blood_group'] = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, required=True)
        self.fields['diocese'] = forms.ChoiceField(choices=DIOCESE_CHOICES, required=True)
        self.fields['mobile'] = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number with country code'}))

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'middle_name',
            'date_of_birth', 'blood_group', 'nid_number', 'passport_number',
            'village', 'parish', 'diocese', 'mobile', 'current_ministry',
            'designation', 'first_profession_date', 'final_profession_date', 'profile_picture' 
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'first_profession_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'final_profession_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'current_ministry': forms.TextInput(attrs={'placeholder': 'Write the name of your Institution/House'}),
            'country': CountrySelectWidget(),
        }
        
    # Override __init__ to customize the blood_group field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blood_group'] = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, required=True)
        self.fields['diocese'] = forms.ChoiceField(choices=DIOCESE_CHOICES, required=True)
        self.fields['mobile'] = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number with country code'}))

class AcademicInformationForm(forms.ModelForm):
    class Meta:
        model = AcademicInformation
        fields = ['degree_name', 'institution_name', 'passing_year', 'gpa']

class ApostolicInformationForm(forms.ModelForm):
    class Meta:
        model = ApostolicInformation
        fields = ['from_date', 'to_date', 'designation', 'apostolate_name', 'is_current']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'to_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
        }

    # Override __init__ to customize help text for `to_date` field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_current'].label = "Still working at this place"
        # Add help text to the 'to_date' field
        self.fields['to_date'].help_text = "Mark the checkbox below if you are still working at this place."
        
    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')
        to_date = cleaned_data.get('to_date')

        if is_current and to_date:
            # If user is still working, clear the to_date field
            self.add_error('to_date', 'To Date must be empty if still working at this place.')

        if not is_current and not to_date:
            # If user is not still working, ensure to_date is provided
            self.add_error('to_date', 'To Date is required if no longer working here.')


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD'}),
        }
        # Explicitly set email to be required
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['email'].required = True


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, 'You have logged in successfully!')
        return super().form_valid(form)
