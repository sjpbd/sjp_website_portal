# appointments/forms.py
from django import forms
from .models import AppointmentLetter, AppointmentAcknowledgment
from tinymce.widgets import TinyMCE
from django.utils.translation import gettext_lazy as _

class AppointmentLetterForm(forms.ModelForm):
    body_text = forms.CharField(widget=TinyMCE())  # Replace CKEditorWidget with TinyMCE

    class Meta:
        model = AppointmentLetter
        fields = [
            'user', 'appointment_type', 'title', 'reference_number',
            'effective_date', 'end_date', 'header_image', 'salutation',
            'body_text', 'new_ministry', 'new_designation', 'ministry_location',
            'signature', 'provincial_name', 'provincial_designation', 'footer_text'
        ]
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter users to show only approved members
        self.fields['user'].queryset = self.fields['user'].queryset.filter(is_approved=True)
        # Add help texts
        self.fields['reference_number'].help_text = _('Unique reference number for this appointment')
        self.fields['end_date'].help_text = _('Optional. Only for temporary appointments')

    def clean(self):
        cleaned_data = super().clean()
        effective_date = cleaned_data.get('effective_date')
        end_date = cleaned_data.get('end_date')
        if end_date and effective_date and end_date <= effective_date:
            raise forms.ValidationError(
                _('End date must be after the effective date.')
            )
        return cleaned_data

class AppointmentAcknowledgmentForm(forms.ModelForm):
    class Meta:
        model = AppointmentAcknowledgment
        fields = ['accepted', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }
