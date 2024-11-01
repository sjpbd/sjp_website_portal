from django.shortcuts import render
from django.http import HttpResponse
from .models import ProvinceLeadership, GeneralLeadership

def leadership_view(request, leadership_type):
    try:
        if leadership_type == 'province':
            leadership = ProvinceLeadership.objects.all()
            template = 'leadership/province_leadership.html'
            context = {'province_leadership': leadership}
        elif leadership_type == 'general':
            leadership = GeneralLeadership.objects.all()
            template = 'leadership/general_leadership.html'
            context = {'general_leadership': leadership, 'show_email': False}
        else:
            return HttpResponse("Invalid leadership type")

        return render(request, template, context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

def province_leadership_view(request):
    try:
        members = ProvinceLeadership.objects.all()
        return render(request, 'leadership/province_leadership.html', {'province_leadership': members})
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

def general_leadership_view(request):
    try:
        members = GeneralLeadership.objects.all()
        context = {
            'general_leadership': members,
            'show_email': False  # Set to False to hide emails
        }
        return render(request, 'leadership/general_leadership.html', context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
