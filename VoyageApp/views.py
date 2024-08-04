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






############################################################################################################################################



#
# def place_info(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     place_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={destination.name}&inputtype=textquery&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     candidates = place_response.get('candidates', [])
#
#     if not candidates:
#         return render(request, 'place_info.html', {'details': None, 'message': 'Place not found'})
#
#     place_id = candidates[0]['place_id']
#
#     details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
#     details_response = requests.get(details_url).json()
#     place_details = details_response.get('result', {})
#
#     nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
#     nearby_response = requests.get(nearby_url).json()
#     nearby_places = nearby_response.get('results', [])
#
#     photos = place_details.get('photos', [])[:4]  # Limit to 4 photos
#     images = [f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo.get('photo_reference')}&key={GOOGLE_API_KEY}" for photo in photos]
#
#     location_link = f"https://www.google.com/maps/search/?api=1&query={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}"
#
#     details = {
#         'name': place_details.get('name', 'Unknown'),
#         'address': place_details.get('formatted_address', 'No address available'),
#         'rating': place_details.get('rating', 'No rating available'),
#         'reviews': place_details.get('reviews', []),
#         'images': images,
#         'location_link': location_link,
#         'nearby_places': nearby_places
#     }
#
#     return render(request, 'place_info.html', {'details': details})


# def search_restaurants(request):
#     location_id = request.GET.get('locationId', '304554')  # Default locationId
#     print("GET request received with locationId:", location_id)
#
#     url = f"https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants?locationId={location_id}"
#     headers = {
#         'x-rapidapi-host': 'tripadvisor16.p.rapidapi.com',
#         'x-rapidapi-key': RAPIDAPI_KEY
#     }
#
#     response = None  # Initialize response to None at the start
#     for attempt in range(3):  # Try up to 3 times with exponential backoff
#         try:
#             response = requests.get(url, headers=headers, timeout=60)  # Increase timeout to 120 seconds
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             data = response.json()
#             print("Data received:", data)  # Debug print to check the structure of the JSON response
#             return render(request, 'itinerary.html', {'data': data['data']})
#         except requests.exceptions.RequestException as e:
#             print(f"Attempt {attempt + 1} failed: {e}")
#             if response is not None:
#                 try:
#                     print(f"Response content: {response.content}")  # Print response content for more details
#                 except Exception as response_error:
#                     print(f"Error accessing response content: {response_error}")
#             if attempt < 2:  # Wait before retrying
#                 wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
#                 print(f"Waiting for {wait_time} seconds before retrying...")
#                 time.sleep(wait_time)
#             else:
#                 return JsonResponse({'error': str(e)}, status=500)
#         except ValueError as json_error:
#             print(f"Error parsing JSON response: {json_error}")
#             return JsonResponse({'error': 'Error parsing JSON response'}, status=500)
#     return JsonResponse({'error': 'Failed to fetch data after multiple attempts'}, status=500)







#
# def place_info(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     place_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={destination.name}&inputtype=textquery&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     candidates = place_response.get('candidates', [])
#
#     if not candidates:
#         return render(request, 'place_info.html', {'details': None, 'message': 'Place not found'})
#
#     place_id = candidates[0]['place_id']
#
#     details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
#     details_response = requests.get(details_url).json()
#     place_details = details_response.get('result', {})
#
#     nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
#     nearby_response = requests.get(nearby_url).json()
#     nearby_places = nearby_response.get('results', [])
#
#     photos = place_details.get('photos', [])
#     images = [f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo.get('photo_reference')}&key={GOOGLE_API_KEY}" for photo in photos]
#
#     details = {
#         'name': place_details.get('name', 'Unknown'),
#         'address': place_details.get('formatted_address', 'No address available'),
#         'rating': place_details.get('rating', 'No rating available'),
#         'reviews': place_details.get('reviews', []),
#         'images': images,
#         'nearby_places': nearby_places
#     }
#
#     return render(request, 'place_info.html', {'details': details})


#
# def place_info(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     place_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={destination.name}&inputtype=textquery&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     candidates = place_response.get('candidates', [])
#
#     if not candidates:
#         return render(request, 'place_info.html', {'details': None, 'message': 'Place not found'})
#
#     place_id = candidates[0]['place_id']
#
#     details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
#     details_response = requests.get(details_url).json()
#     place_details = details_response.get('result', {})
#
#     nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
#     nearby_response = requests.get(nearby_url).json()
#     nearby_places = nearby_response.get('results', [])
#
#     details = {
#         'name': place_details.get('name', 'Unknown'),
#         'address': place_details.get('formatted_address', 'No address available'),
#         'website': place_details.get('website', 'No website available'),
#         'rating': place_details.get('rating', 'No rating available'),
#         'reviews': place_details.get('reviews', []),
#         'image_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_details.get('photos', [{}])[0].get('photo_reference', '')}&key={GOOGLE_API_KEY}" if place_details.get('photos') else None,
#         'map_url': f"https://www.google.com/maps/place/?q=place_id:{place_id}",
#         'nearby_places': nearby_places
#     }
#
#     return render(request, 'place_info.html', {'details': details})


# def place_info(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     place_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={destination.name}&inputtype=textquery&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     candidates = place_response.get('candidates', [])
#
#     if not candidates:
#         return render(request, 'place_info.html', {'details': None, 'message': 'Place not found'})
#
#     place_id = candidates[0]['place_id']
#
#     details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
#     details_response = requests.get(details_url).json()
#     place_details = details_response.get('result', {})
#
#     nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
#     nearby_response = requests.get(nearby_url).json()
#     nearby_places = nearby_response.get('results', [])
#
#     details = {
#         'name': place_details.get('name', 'Unknown'),
#         'address': place_details.get('formatted_address', 'No address available'),
#         'phone_number': place_details.get('formatted_phone_number', 'No phone number available'),
#         'website': place_details.get('website', 'No website available'),
#         'rating': place_details.get('rating', 'No rating available'),
#         'reviews': place_details.get('reviews', []),
#         'image_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_details.get('photos', [{}])[0].get('photo_reference', '')}&key={GOOGLE_API_KEY}" if place_details.get('photos') else None,
#         'nearby_places': nearby_places
#     }
#
#     return render(request, 'place_info.html', {'details': details})

#
# def place_info(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     place_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={destination.location}&inputtype=textquery&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     candidates = place_response.get('candidates', [])
#
#     if not candidates:
#         return render(request, 'place_info.html', {'details': None, 'message': 'Place not found'})
#
#     place_id = candidates[0]['place_id']
#
#     details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
#     details_response = requests.get(details_url).json()
#     place_details = details_response.get('result', {})
#
#     nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
#     nearby_response = requests.get(nearby_url).json()
#     nearby_places = nearby_response.get('results', [])
#
#     details = {
#         'name': place_details.get('name', 'Unknown'),
#         'address': place_details.get('formatted_address', 'No address available'),
#         'phone_number': place_details.get('formatted_phone_number', 'No phone number available'),
#         'website': place_details.get('website', 'No website available'),
#         'rating': place_details.get('rating', 'No rating available'),
#         'reviews': place_details.get('reviews', []),
#         'image_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_details.get('photos', [{}])[0].get('photo_reference', '')}&key={GOOGLE_API_KEY}" if place_details.get(
#             'photos') else None,
#         'nearby_places': nearby_places
#     }
#
#     return render(request, 'place_info.html', {'details': details})

 # Replace with your actual Google API key

# def place_info(request, place_id):
#     place_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     place_details = place_response.get('result', {})
#
#     nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={place_details.get('geometry', {}).get('location', {}).get('lat')},{place_details.get('geometry', {}).get('location', {}).get('lng')}&radius=1500&type=point_of_interest&key={GOOGLE_API_KEY}"
#     nearby_response = requests.get(nearby_url).json()
#     nearby_places = nearby_response.get('results', [])
#
#     details = {
#         'name': place_details.get('name', 'Unknown'),
#         'address': place_details.get('formatted_address', 'No address available'),
#         'phone_number': place_details.get('formatted_phone_number', 'No phone number available'),
#         'website': place_details.get('website', 'No website available'),
#         'rating': place_details.get('rating', 'No rating available'),
#         'reviews': place_details.get('reviews', []),
#         'image_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_details.get('photos', [{}])[0].get('photo_reference', '')}&key={GOOGLE_API_KEY}" if place_details.get('photos') else None,
#         'nearby_places': nearby_places
#     }
#
#     return render(request, 'place_info.html', {'details': details})

# def search_restaurants(request):
#     location_id = request.GET.get('locationId', 'ChIJOwg_06VPwokRYv534QaPC8g')  # Default to New York City Place ID
#     print("GET request received with locationId:", location_id)
#
#     # url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_id}&radius=1500&type=restaurant&key={GOOGLE_API_KEY}"
#     url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7128,-74.0060&radius=1500&type=restaurant&key=YOUR_GOOGLE_API_KEY"
#     response = None  # Initialize response to None at the start
#     for attempt in range(3):  # Try up to 3 times with exponential backoff
#         try:
#             response = requests.get(url, timeout=60)  # Increase timeout to 60 seconds
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             data = response.json()
#             print("Data received:", data)  # Debug print to check the structure of the JSON response
#             if 'results' in data:
#                 return render(request, 'itinerary.html', {'data': data['results']})
#             else:
#                 print("No 'results' found in the response")
#                 return JsonResponse({'error': 'No results found'}, status=404)
#         except requests.exceptions.RequestException as e:
#             print(f"Attempt {attempt + 1} failed: {e}")
#             if response is not None:
#                 try:
#                     print(f"Response content: {response.content}")  # Print response content for more details
#                 except Exception as response_error:
#                     print(f"Error accessing response content: {response_error}")
#             if attempt < 2:  # Wait before retrying
#                 wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
#                 print(f"Waiting for {wait_time} seconds before retrying...")
#                 time.sleep(wait_time)
#             else:
#                 return JsonResponse({'error': str(e)}, status=500)
#         except ValueError as json_error:
#             print(f"Error parsing JSON response: {json_error}")
#             return JsonResponse({'error': 'Error parsing JSON response'}, status=500)
#     return JsonResponse({'error': 'Failed to fetch data after multiple attempts'}, status=500)

#
# def destination_detail(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     # Fetch place details from Google Places API
#     place_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={destination.place_id}&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     place_details = place_response.get('result', {})
#
#     # Extract relevant details
#     details = {
#         'name': destination.name,
#         'description': place_details.get('description', 'No description available'),
#         'image_url': place_details.get('photos', [{}])[0].get('photo_reference', ''),
#         'map_url': f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_API_KEY}&q={destination.location}",
#         'nearby_places': place_details.get('nearby_places', []),
#     }
#
#     return render(request, 'destination.html', {'details': details})

# def destination_detail(request, pk):
#     destination = get_object_or_404(Destination, pk=pk)
#
#     # Fetch place details from Google Places API
#     place_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={destination.place_id}&key={GOOGLE_API_KEY}"
#     place_response = requests.get(place_url).json()
#     place_details = place_response.get('result', {})
#
#     # Extract relevant details
#     details = {
#         'name': destination.name,
#         'description': place_details.get('editorial_summary', {}).get('overview', 'No description available'),
#         'image_url': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_details.get('photos', [{}])[0].get('photo_reference', '')}&key={GOOGLE_API_KEY}",
#         'map_url': f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_API_KEY}&q=place_id:{destination.place_id}",
#         'nearby_hotels': [place.get('name', 'Unknown') for place in place_details.get('hotel', [])],
#         'places_to_discover': [place.get('name', 'Unknown') for place in place_details.get('places_to_discover', [])],
#     }
#
#     return render(request, 'destnation.html', {'destination': destination, 'details': details})