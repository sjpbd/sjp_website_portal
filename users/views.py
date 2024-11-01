# users/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm, CustomUserChangeForm, AcademicInformationForm, ApostolicInformationForm
from .models import AcademicInformation, ApostolicInformation, CustomUser
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Q
from .decorators import user_must_be_approved
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import CustomUser  
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            messages.success(request, 'Your account has been created successfully!')
            if user.is_approved:
                return redirect('users:dashboard')
            else:
                messages.info(request, 'Your profile is under review. Once approved by the admin, you will be able to access the dashboard.')
                return redirect('users:under_review')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def under_review(request):
    if request.user.is_authenticated and request.user.is_approved:
        return redirect('users:dashboard')
    return render(request, 'users/under_review.html')

class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_approved:
            messages.success(self.request, 'You have logged in successfully!')
            return response
        else:
            messages.warning(self.request, 'Your profile is under review. Once approved by the admin, you will be able to access the dashboard.')
            return redirect('users:under_review')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_must_be_approved
def dashboard(request):
    return render(request, 'users/dashboard.html')

@user_must_be_approved
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:dashboard')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})

@user_must_be_approved
def add_academic_info(request):
    if request.method == 'POST':
        form = AcademicInformationForm(request.POST)
        if form.is_valid():
            academic_info = form.save(commit=False)
            academic_info.user = request.user
            academic_info.save()
            # Add success message
            messages.success(request, "Academic information added successfully.")
            return redirect('users:dashboard')  # Redirect to the page where you want the message to appear
    else:
        form = AcademicInformationForm()

    return render(request, 'users/add_academic_info.html', {'form': form})

@user_must_be_approved
def add_apostolic_info(request):
    if request.method == 'POST':
        form = ApostolicInformationForm(request.POST)
        if form.is_valid():
            apostolic_info = form.save(commit=False)
            apostolic_info.user = request.user
            apostolic_info.save()
            # Add success message
            messages.success(request, "Apostolic information added successfully.")
            return redirect('users:dashboard')  # Redirect to the page where you want the message to appear
    else:
        form = ApostolicInformationForm()

    return render(request, 'users/add_apostolic_info.html', {'form': form})


@user_must_be_approved
def edit_academic_info(request, pk):
    academic_info = get_object_or_404(AcademicInformation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AcademicInformationForm(request.POST, instance=academic_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic information updated successfully.')
            return redirect('users:dashboard')
    else:
        form = AcademicInformationForm(instance=academic_info)

    return render(request, 'users/edit_academic_info.html', {
        'form': form,
        'object': academic_info  # Ensure this variable is passed to the template
    })
@user_must_be_approved
def delete_academic_info(request, pk):
    academic_info = get_object_or_404(AcademicInformation, pk=pk, user=request.user)
    if request.method == 'POST':
        academic_info.delete()
        messages.success(request, 'Academic information deleted successfully.')
        return redirect('users:dashboard')
    return HttpResponseForbidden("You don't have permission to delete this.")


@user_must_be_approved
def edit_apostolic_info(request, pk):
    apostolic_info = get_object_or_404(ApostolicInformation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApostolicInformationForm(request.POST, instance=apostolic_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apostolic information updated successfully.')
            return redirect('users:dashboard')
    else:
        form = ApostolicInformationForm(instance=apostolic_info)

    return render(request, 'users/edit_apostolic_info.html', {
        'form': form,
        'object': apostolic_info  # Ensure this variable is passed to the template
    })


@user_must_be_approved
def update_apostolic_info(request, pk):
    apostolic_info = get_object_or_404(ApostolicInformation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApostolicInformationForm(request.POST, instance=apostolic_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apostolic information updated successfully.')
            return redirect('users:dashboard')
    else:
        form = ApostolicInformationForm(instance=apostolic_info)

    return render(request, 'users/edit_apostolic_info.html', {
        'form': form,
        'object': apostolic_info  # Ensure this variable is passed to the template
    })


@user_must_be_approved
def delete_apostolic_info(request, pk):
    apostolic_info = get_object_or_404(ApostolicInformation, pk=pk, user=request.user)
    apostolic_info.delete()
    messages.success(request, 'Apostolic information deleted successfully.')
    return redirect('users:dashboard')


class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have logged out successfully!')
        return super().dispatch(request, *args, **kwargs)



@user_must_be_approved
def upload_profile_picture(request):
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            # Validate file type
            if profile_picture.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                messages.error(request, 'Unsupported file type. Please upload a JPEG, PNG, or GIF image.')
                return redirect('users:upload_profile_picture')  # Redirect to the same page
            
            user = request.user
            user.profile_picture = profile_picture
            user.save()
            messages.success(request, 'Profile picture uploaded successfully!')
            return redirect('users:dashboard')  # Redirect to the appropriate URL after upload
        else:
            messages.error(request, 'Please upload a valid image file.')
    
    # If the request method is GET or if there's an error, render the upload template
    return render(request, 'users/dashboard.html')  # Ensure the correct template path



class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        messages.success(self.request, 'You have logged in successfully!')
        return super().form_valid(form)


@user_must_be_approved
def brothers_contacts(request):
    query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', 'name')
    
    # Filter users based on search query
    users = CustomUser.objects.filter(
        Q(first_name__icontains=query) |
        Q(middle_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(mobile__icontains=query)
    )
    
    # Sort users based on the selected sort option
    if sort_option == 'name':
        users = users.order_by('first_name')
    elif sort_option == 'name_reverse':
        users = users.order_by('-first_name')
    elif sort_option == 'age':
        users = users.order_by('date_of_birth')
    elif sort_option == 'age_reverse':
        users = users.order_by('-date_of_birth')
    
    return render(request, 'users/brothers_contacts.html', {'users': users, 'query': query, 'sort_option': sort_option})



@method_decorator(user_must_be_approved, name='dispatch')
class MainPageView(TemplateView):
    template_name = 'users/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        today_day = today.day
        today_month = today.month

        if self.request.user.is_authenticated and not self.request.user.is_approved:
            messages.warning(self.request, 'Your profile is under review. Once approved by the admin, you will be able to access all features.')

        # Users with birthdays today (match day and month only)
        context['birthday_users'] = CustomUser.objects.filter(
            date_of_birth__day=today_day,
            date_of_birth__month=today_month
        )

        # Users with first profession anniversary today
        context['first_profession_users'] = CustomUser.objects.filter(
            first_profession_date__day=today_day,
            first_profession_date__month=today_month
        )

        # Users with final profession anniversary today
        context['final_profession_users'] = CustomUser.objects.filter(
            final_profession_date__day=today_day,
            final_profession_date__month=today_month
        )

        return context





