# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class ApprovalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require approval
        exempt_urls = [
            reverse('users:login'),
            reverse('users:signup'),
            reverse('users:under_review'),
            reverse('users:logout'),
            '/admin/',  # Django admin
            '/static/',  # Static files
            '/media/',  # Media files
        ]

        # Check if the current URL is exempt
        if not any(request.path.startswith(url) for url in exempt_urls):
            if request.user.is_authenticated and not request.user.is_approved:
                messages.warning(request, 'Your profile is under review. Once approved by the admin, you will be able to access all features.')
                return redirect('users:under_review')

        response = self.get_response(request)
        return response