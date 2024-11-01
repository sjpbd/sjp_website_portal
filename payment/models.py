# payment/models.py
from django.db import models
from django.conf import settings

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('VISA', 'Visa Card'),
        ('MASTER', 'Master Card'),
        ('AMEX', 'American Express'),
        ('BKASH-BKash', 'bKash'),
        ('NAGAD-Nagad', 'Nagad'),
        ('ROCKET-Rocket', 'Rocket'),
    ]
    
    CURRENCY_CHOICES = [
        ('BDT', 'Bangladeshi Taka'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='BDT')
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    
    # Customer information with default values
    customer_name = models.CharField(max_length=255, default='')
    customer_email = models.EmailField(default='')
    customer_phone = models.CharField(max_length=15, default='')
    customer_address = models.TextField(default='')
    customer_city = models.CharField(max_length=100, default='')
    customer_postcode = models.CharField(max_length=10, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.user.username} - {self.amount} {self.currency} - {self.status}"
    
    def __str__(self):
        return f"Payment by {self.user.username if self.user else 'Anonymous'} - {self.transaction_id}"
