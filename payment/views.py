from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm
import uuid
import requests
import logging

logger = logging.getLogger(__name__)

def initiate_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            
            # Handle user assignment
            if request.user.is_authenticated:
                payment.user = request.user
            else:
                # For anonymous users, set user to None (ensure your model allows this)
                payment.user = None
            
            payment.transaction_id = str(uuid.uuid4())
            
            # SSL Commerz integration with all required fields
            post_data = {
                'store_id': settings.SSLCOMMERZ_STORE_ID,
                'store_passwd': settings.SSLCOMMERZ_STORE_PASS,
                'total_amount': float(payment.amount),
                'currency': payment.currency,
                'tran_id': payment.transaction_id,
                'success_url': request.build_absolute_uri(reverse('payment:success')),
                'fail_url': request.build_absolute_uri(reverse('payment:fail')),
                'cancel_url': request.build_absolute_uri(reverse('payment:cancel')),
                'emi_option': '0',
                'cus_name': payment.customer_name,
                'cus_email': payment.customer_email,
                'cus_phone': payment.customer_phone,
                'cus_add1': payment.customer_address,
                'cus_city': payment.customer_city,
                'cus_postcode': payment.customer_postcode,
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'Donation',
                'product_category': 'Donation',
                'product_profile': 'non-physical-goods',
                'multi_card_name': payment.payment_method,
            }

            try:
                response = requests.post(
                    settings.SSLCOMMERZ_PAYMENT_URL,
                    data=post_data,
                    verify=True
                )
                response_data = response.json()
                
                if response_data.get('status') == 'SUCCESS':
                    payment.save()  # Only save if SSLCommerz request is successful
                    return redirect(response_data['GatewayPageURL'])
                else:
                    logger.error(f"Payment initiation failed: {response_data}")
                    messages.error(request, f'Payment initiation failed: {response_data.get("failedreason", "Unknown error")}')
            
            except Exception as e:
                logger.error(f"Payment error: {str(e)}")
                messages.error(request, f'Payment error: {str(e)}')
        
        else:
            logger.error(f"Form validation errors: {form.errors}")
            messages.error(request, 'Please correct the errors in the form.')
    
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data.update({
                'customer_name': request.user.get_full_name(),
                'customer_email': request.user.email,
            })
        form = PaymentForm(initial=initial_data)
    
    return render(request, 'payment/initiate_payment.html', {'form': form})

@csrf_exempt
def payment_success(request):
    try:
        payment = Payment.objects.get(transaction_id=request.POST['tran_id'])
        payment.status = 'COMPLETED'
        payment.payment_method = request.POST.get('card_type', payment.payment_method)
        payment.save()
        messages.success(request, 'Payment completed successfully!')
        return render(request, 'payment/success.html', {'payment': payment})
    except Payment.DoesNotExist:
        messages.error(request, 'Invalid transaction.')
        return redirect('payment:initiate')

@csrf_exempt
def payment_fail(request):
    try:
        payment = Payment.objects.get(transaction_id=request.POST['tran_id'])
        payment.status = 'FAILED'
        payment.save()
        messages.error(request, 'Payment failed.')
        return render(request, 'payment/fail.html', {'payment': payment})
    except Payment.DoesNotExist:
        messages.error(request, 'Invalid transaction.')
        return redirect('payment:initiate')

@csrf_exempt
def payment_cancel(request):
    try:
        payment = Payment.objects.get(transaction_id=request.POST['tran_id'])
        payment.status = 'FAILED'
        payment.save()
        messages.info(request, 'Payment cancelled.')
        return render(request, 'payment/cancel.html', {'payment': payment})
    except Payment.DoesNotExist:
        messages.error(request, 'Invalid transaction.')
        return redirect('payment:initiate')
