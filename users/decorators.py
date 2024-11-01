from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.urls import reverse

def user_must_be_approved(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('users:login')  # Redirect to the login page
        
        # Check if the user is approved
        if not request.user.is_approved:
            messages.warning(request, 'Your profile is under review. Once approved by the admin, you will be able to access this page.')
            return redirect('users:under_review')  # Redirect to the under review page
            
        return view_func(request, *args, **kwargs)  # Call the original view function

    return _wrapped_view
