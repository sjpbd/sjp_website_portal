#brothers_profile/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO
from .models import Profile, ReligiousInfo, AcademicRecord, Experience, Publication, SocialLink
from .forms import ProfileForm, ReligiousInfoForm, AcademicRecordForm, ExperienceForm, PublicationForm, SocialLinkForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from haystack.query import SearchQuerySet
import base64
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy

from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import ProfileSerializer

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        # Log in the user
        login(self.request, form.get_user())

        # Add a success message
        messages.success(self.request, 'You have successfully logged in!')

        # Redirect to the profile details page
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Redirect to the specific user's profile details page
        return reverse_lazy('brothers_profile:profile_details', kwargs={'user_id': self.request.user.id})



@csrf_exempt
def clear_academic_records(request):
    if request.method == 'POST':
        AcademicRecord.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_protect
def profile_create_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    religious_info, _ = ReligiousInfo.objects.get_or_create(profile=profile)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        religious_info_form = ReligiousInfoForm(request.POST, instance=religious_info)
        academic_record_form = AcademicRecordForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        publication_form = PublicationForm(request.POST)
        social_link_form = SocialLinkForm(request.POST)

        if all([profile_form.is_valid(), religious_info_form.is_valid(), 
                academic_record_form.is_valid(), experience_form.is_valid(), 
                publication_form.is_valid(), social_link_form.is_valid()]):
            
            profile = profile_form.save(commit=False)
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            
            religious_info_form.save()
            
            academic_record = academic_record_form.save(commit=False)
            academic_record.profile = profile
            academic_record.save()

            experience = experience_form.save(commit=False)
            experience.profile = profile
            experience.save()

            publication = publication_form.save(commit=False)
            publication.profile = profile
            publication.save()

            social_link = social_link_form.save(commit=False)
            social_link.profile = profile
            social_link.save()

            return JsonResponse({'success': True, 'redirect_url': reverse('brothers_profile:profile_view')})
    else:
        profile_form = ProfileForm(instance=profile)
        religious_info_form = ReligiousInfoForm(instance=religious_info)
        academic_record_form = AcademicRecordForm()
        experience_form = ExperienceForm()
        publication_form = PublicationForm()
        social_link_form = SocialLinkForm()

    context = {
        'profile_form': profile_form,
        'religious_info_form': religious_info_form,
        'academic_record_form': academic_record_form,
        'experience_form': experience_form,
        'publication_form': publication_form,
        'social_link_form': social_link_form,
    }

    return render(request, 'brothers_profile/profile_form.html', context)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if not profile.profile_picture:
        profile.profile_picture = None

    religious_info, _ = ReligiousInfo.objects.get_or_create(profile=profile)
    academic_records = AcademicRecord.objects.filter(profile=profile)
    experiences = Experience.objects.filter(profile=profile)
    publications = Publication.objects.filter(profile=profile)
    social_links = SocialLink.objects.filter(profile=profile)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('brothers_profile:profile_view')

    context = {
        'profile': profile,
        'religious_info': religious_info,
        'academic_records': academic_records,
        'experiences': experiences,
        'publications': publications,
        'social_links': social_links,
        'profile_form': ProfileForm(instance=profile)
    }
    return render(request, 'brothers_profile/profile.html', context)

@login_required
@csrf_protect
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        religious_form = ReligiousInfoForm(request.POST, instance=request.user.profile.religiousinfo)
        if profile_form.is_valid() and religious_form.is_valid():
            profile_form.save()
            religious_form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
@csrf_protect
def add_academic_record(request):
    if request.method == 'POST':
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.profile = request.user.profile
            record.save()
            return JsonResponse({'status': 'success', 'id': record.id})
    return JsonResponse({'status': 'error'})

@login_required
@csrf_protect
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = request.user.profile
            experience.save()
            return JsonResponse({'status': 'success', 'id': experience.id})
    return JsonResponse({'status': 'error'})

@login_required
@csrf_protect
def add_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.profile = request.user.profile
            publication.save()
            return JsonResponse({'status': 'success', 'id': publication.id})
    return JsonResponse({'status': 'error'})

@login_required
@csrf_protect
def update_social_links(request):
    if request.method == 'POST':
        SocialLink.objects.filter(profile=request.user.profile).delete()
        for platform, url in request.POST.items():
            if platform.startswith('social_') and url:
                SocialLink.objects.create(profile=request.user.profile, platform=platform[7:], url=url)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def export_to_pdf(request):
    profile = get_object_or_404(Profile, user=request.user)
    religious_info = get_object_or_404(ReligiousInfo, profile=profile)
    academic_records = AcademicRecord.objects.filter(profile=profile)
    experiences = Experience.objects.filter(profile=profile)
    publications = Publication.objects.filter(profile=profile)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Add a title
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=1,
        spaceAfter=12
    )
    title = Paragraph(f"Profile: {profile.user.username}", title_style)
    elements.append(title)
    
    # Profile Information Table
    profile_data = [
        ['Full Name', f"{profile.first_name} {profile.middle_name} {profile.last_name}"],
        ['Date of Birth', profile.date_of_birth or 'N/A'],
        ['Place of Birth', profile.place_of_birth or 'N/A'],
        ['Mobile Number', profile.mobile_number or 'N/A'],
        ['Email Address', profile.email_address or 'N/A'],
        ['Father\'s Name', profile.father_name or 'N/A'],
        ['Mother\'s Name', profile.mother_name or 'N/A'],
        ['Parish Name', profile.parish_name or 'N/A'],
        ['Village Name', profile.village_name or 'N/A'],
        ['District Name', profile.dist_name or 'N/A'],
        ['Blood Group', profile.blood_group or 'N/A'],
        ['Passport Number', profile.passport_number or 'N/A'],
        ['NID Number', profile.nid_number or 'N/A'],
        ['Religion', religious_info.religion or 'N/A']
    ]
    profile_table = Table(profile_data)
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(profile_table)
    
    # Academic Records Table
    academic_data = [['Degree', 'Institution', 'Year', 'Details']]
    for record in academic_records:
        academic_data.append([
            record.degree,
            record.institution,
            record.year,
            record.details
        ])
    academic_table = Table(academic_data)
    academic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(academic_table)
    
    # Experiences Table
    experience_data = [['Organization', 'Role', 'Start Date', 'End Date', 'Details']]
    for exp in experiences:
        experience_data.append([
            exp.organization,
            exp.role,
            exp.start_date,
            exp.end_date,
            exp.details
        ])
    experience_table = Table(experience_data)
    experience_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(experience_table)
    
    # Publications Table
    publication_data = [['Title', 'Publisher', 'Date', 'Details']]
    for pub in publications:
        publication_data.append([
            pub.title,
            pub.publisher,
            pub.date,
            pub.details
        ])
    publication_table = Table(publication_data)
    publication_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(publication_table)
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="profile_{profile.user.username}.pdf"'
    return response


def search_view(request):
    query = request.GET.get('q', '')
    print(f"Query: {query}")
    if query:
        results = SearchQuerySet().models(Profile).autocomplete(content_auto=query)
        print(f"Results: {results}")
        profiles = [r.object for r in results]
    else:
        profiles = []
    
    context = {
        'query': query,
        'profiles': profiles,
    }
    return render(request, 'brothers_profile/search_results.html', context)

def profile_details(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    context = {'profile': profile}
    return render(request, 'brothers_profile/profile_detail.html', context)
    

@api_view(['POST'])
def api_profile_update(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'})
    return Response(serializer.errors, status=400)

