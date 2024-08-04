from django.shortcuts import render, redirect, get_object_or_404
import requests 
from .models import Destination, UserPreference
from .forms import UserPreferenceForm
import requests
from django.shortcuts import render, get_object_or_404
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
print("GOOGLE_API_KEY:", GOOGLE_API_KEY)  # Debugging output
def index(request):
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST)
        if form.is_valid():
            user_preference = form.save()
            return redirect('results', pk=user_preference.pk)
    else:
        form = UserPreferenceForm()
    return render(request, 'index.html', {'form': form})

def results(request, pk):
    user_preference = get_object_or_404(UserPreference, pk=pk)
    matching_destinations = Destination.objects.filter(
        type=user_preference.destination_type,
        budget=user_preference.budget
    )
    return render(request, 'results.html', {'destinations': matching_destinations})

def place_info(request, pk):
    destination = get_object_or_404(Destination, pk=pk)

    place_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={destination.name}&inputtype=textquery&key={GOOGLE_API_KEY}"
    place_response = requests.get(place_url).json()
    candidates = place_response.get('candidates', [])

    if not candidates:
        return render(request, 'place_info.html', {'details': None, 'message': 'Place not found'})

    place_id = candidates[0]['place_id']

    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
    details_response = requests.get(details_url).json()
    place_details = details_response.get('result', {})

    nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
    nearby_response = requests.get(nearby_url).json()
    nearby_places = nearby_response.get('results', [])

    details = {
        'name': place_details.get('name', 'Unknown'),
        'address': place_details.get('formatted_address', 'No address available'),
        'rating': place_details.get('rating', 'No rating available'),
        'reviews': place_details.get('reviews', []),
        'location_link': f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={place_id}",
        'images': [f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={GOOGLE_API_KEY}" for photo in place_details.get('photos', [])[:4]],
        'nearby_places': [{'name': place['name']} for place in nearby_places]
    }

    return render(request, 'place_info.html', {'details': details})



