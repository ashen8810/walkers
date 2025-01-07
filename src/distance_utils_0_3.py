import requests
import json
import itertools
from geopy.distance import geodesic

def geocodes(city):
    headers = {
        "User-Agent": "YourAppName/1.0 (your.email@example.com)"
    }
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/search?q={city}&format=json", headers=headers)
        
        data = json.loads(response.content)
        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            print(f"No coordinates found for {city}")
            return None, None
    except Exception as e:
        print(f"Error geocoding {city}: {e}")
        return None, None

def calculate_distances(selected_locations):
    """Calculate distances between selected locations."""
    coordinates = {}
    for location, *_ in selected_locations:
        lat, lon = geocodes(location)
        if lat is not None and lon is not None:
            coordinates[location] = (lat, lon)
        else:
            print(f"Could not find coordinates for {location}")
            return None

    distances = {}
    for i in range(len(selected_locations)):
        for j in range(i + 1, len(selected_locations)):
            loc1, *_ = selected_locations[i]
            loc2, *_ = selected_locations[j]
            distance = geodesic(coordinates[loc1], coordinates[loc2]).km
            distances[(loc1, loc2)] = distance
            distances[(loc2, loc1)] = distance  # Add reverse direction
    
    return distances, coordinates


def find_shortest_path(selected_locations):
    # Check if Colombo is in the locations
    colombo_exists = any(loc == "colombo" for loc, *_ in selected_locations)
    
    # If Colombo is not in the list, add it
    if not colombo_exists:
        selected_locations.insert(0, ("colombo", 1))
    
    # Calculate distances between locations
    distances_result = calculate_distances(selected_locations)
    
    if distances_result is None:
        return None, None
    
    distances, coordinates = distances_result
    
    locations = [loc for loc, *_ in selected_locations]
    
    # Ensure Colombo is the first location
    start_location = "colombo"
    locations.remove(start_location)
    
    # Try all possible permutations of remaining locations
    shortest_distance = float('inf')
    shortest_path = None
    
    for path in itertools.permutations(locations):
        full_path = (start_location,) + path  # Include Colombo at the start
        
        total_distance = 0
        for i in range(len(full_path) - 1):
            total_distance += distances.get((full_path[i], full_path[i + 1]), float('inf'))
        
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = full_path
    
    return list(reversed(shortest_path)), shortest_distance
