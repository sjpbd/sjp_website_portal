# map_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SearchForm
from .models import Search, Ministry
import folium
import requests
from django.conf import settings
import json

def geocode(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1
    }
    headers = {
        'User-Agent': f'YourAppName/{settings.VERSION} (your@email.com)'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            result = data[0]
            lat, lon = float(result['lat']), float(result['lon'])
            country = result['address'].get('country', '')
            if country.lower() != address.lower() and address.lower() not in country.lower():
                raise ValueError(f"Geocoding result doesn't match the expected country: {country}")
            return lat, lon, country
    except requests.RequestException as e:
        print(f"Geocoding API error: {e}")
    except ValueError as e:
        print(f"Geocoding accuracy error: {e}")
    except Exception as e:
        print(f"Unexpected geocoding error: {e}")
    return None, None, None

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('map_app:index')
    else:
        form = SearchForm()

    # Create a default map centered on Bangladesh
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7)

    # Add markers for all ministries
    ministries = Ministry.objects.all()
    for ministry in ministries:
        popup_content = f"""
        <strong>{ministry.name}</strong><br>
        Type: {ministry.get_ministry_type_display()}<br>
        Address: {ministry.address}<br>
        {ministry.description}
        """
        folium.Marker(
            [ministry.latitude, ministry.longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=ministry.name,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    # Handle search functionality
    address = Search.objects.last()
    if address:
        lat, lon, country = geocode(address.address)
        if lat and lon:
            folium.Marker(
                [lat, lon],
                tooltip='Search Result',
                popup=f"{address.address}, {country}",
                icon=folium.Icon(color='green', icon='search')
            ).add_to(m)
            m.location = [lat, lon]
            m.zoom_start = 10
            messages.success(request, f"Location found: {address.address}, {country}")
        else:
            messages.error(request, f"Couldn't find accurate location for: {address.address}")

    # Get HTML Representation of Map Object
    map_html = m._repr_html_()
    context = {
        'map': map_html,
        'form': form,
    }
    return render(request, 'map_app/index.html', context)