from django import forms
from .models import Payment
from django.core.validators import RegexValidator, MinValueValidator

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'amount',
            'currency',
            'payment_method',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'customer_city',
            'customer_postcode'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update widgets and attributes for all fields
        for field in self.fields:
            if field != 'payment_method':  # Avoid adding form-control to radio buttons
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.replace('_', ' ').title()
                })

        # Special handling for amount field
        self.fields['amount'].widget.attrs.update({
            'min': '1',
            'step': '0.01',
            'placeholder': 'Enter amount'
        })

        # Set up payment method as radio buttons
        self.fields['payment_method'].widget = forms.RadioSelect(
            attrs={'class': 'form-check-input'}
        )
        
        # Make all fields required
        for field_name, field in self.fields.items():
            field.required = True

        # Update help text for international phone format
        self.fields['customer_phone'].help_text = "Enter phone number in international format, e.g., +11234567890"
        
        # Validator for international phone numbers (7 to 15 digits, allowing + at start)
        self.fields['customer_phone'].validators = [
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message='Enter a valid international phone number, including country code'
            )
        ]
        
        # Validator for minimum amount
        self.fields['amount'].validators = [
            MinValueValidator(
                1,
                message='Amount must be at least 1'
            )
        ]

    def clean_currency(self):
        currency = self.cleaned_data.get('currency')
        if currency not in [choice[0] for choice in Payment.CURRENCY_CHOICES]:
            raise forms.ValidationError('Invalid currency selection')
        return currency

    def clean_payment_method(self):
        payment_method = self.cleaned_data.get('payment_method')
        if payment_method not in [choice[0] for choice in Payment.PAYMENT_METHOD_CHOICES]:
            raise forms.ValidationError('Invalid payment method selection')
        return payment_method

    def clean_customer_email(self):
        email = self.cleaned_data.get('customer_email')
        if not email:
            raise forms.ValidationError('Email is required')
        return email.lower()  # Normalize email to lowercase

    def clean(self):
        cleaned_data = super().clean()
        
        amount = cleaned_data.get('amount')
        currency = cleaned_data.get('currency')
        
        # Validation for minimum amounts based on currency
        if amount and currency:
            if currency == 'BDT' and amount < 10:
                raise forms.ValidationError(
                    'Minimum amount for BDT payments is 10 BDT'
                )
            elif currency != 'BDT' and amount < 1:
                raise forms.ValidationError(
                    'Minimum amount for foreign currency payments is 1'
                )
        
        return cleaned_data
