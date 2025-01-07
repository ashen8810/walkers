# location_analysis.py
def calculate_location_percentage_by_tour(itinerary, locations, duration):
    """Calculate location matching percentages for each tour."""
    filtered_itinerary = itinerary[itinerary['days'] == duration]
    locations = [loc.lower() for loc in locations]

    tour_location_percentages = {}
    for tour_title, tour_data in itinerary.groupby('tour_title'):
        unique_tour_locations = tour_data['location'].unique().tolist()
        matching_locations = [loc for loc in locations if loc in unique_tour_locations]
        
        percentage = (len(matching_locations) / max(len(unique_tour_locations), len(locations))) * 100
        tour_location_percentages[tour_title] = {
            'percentage': percentage,
            'matched_locations': matching_locations
        }
    return tour_location_percentages

def find_best_tour(results):
    """Find the best matching tour."""
    best_tour = None
    min_difference = 100

    for tour, data in results.items():
        difference = abs(data['percentage'] - 100)
        if difference == 0:
            return tour
        if difference < min_difference:
            min_difference = difference
            best_tour = tour
        elif difference == min_difference and data['percentage'] > results.get(best_tour, {}).get('percentage', 0):
            best_tour = tour
    return best_tour

def calculate_day_counts_by_location(itinerary, locations, tour_title):
    filtered_itinerary = itinerary[itinerary['tour_title'] == tour_title]
    unique_days = filtered_itinerary.drop_duplicates(['location','day'])
    location_day_count = unique_days.groupby("location")["day"].count()
    return location_day_count.to_dict()

def find_best_tour_with_days(itinerary_file, locations, duration):
    result = calculate_location_percentage_by_tour(itinerary_file, locations, duration)
    best_match = find_best_tour(result)
    day_counts = calculate_day_counts_by_location(itinerary_file, locations, best_match)
    
    
    # Initialize location days with 0
    location_days = {loc.lower(): 0 for loc in locations}
    
    current_duration = 0
    selected_locations = []

    sorted_locations = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
    
    # First pass: allocate full days to matching locations
    for location, days in sorted_locations:
        if location in location_days:
            # Allocate full days while not exceeding total duration
            allocatable_days = min(days, duration - current_duration)
            location_days[location] = allocatable_days
            current_duration += allocatable_days
            selected_locations.append((location, allocatable_days))
            
            # Break if we've reached the exact duration
            if current_duration == duration:
                break
    
    selected_location_names = [loc[0] for loc in selected_locations]
    missing_locations = [loc for loc in locations if loc not in selected_location_names]
    i=0
    while (current_duration != duration) or len(missing_locations) != 0:
      selected_cities = [city for city, _ in selected_locations]
      missing_locations = [city for city in locations if city not in selected_cities]
      if current_duration < duration:
        lowest_location = min(selected_locations, key=lambda x: x[1])
        index = selected_locations.index(lowest_location)
        selected_locations[index] = (lowest_location[0], lowest_location[1] + 1)
        current_duration += 1
      elif current_duration > duration:
        lowest_location = max(selected_locations, key=lambda x: x[1])
        index = selected_locations.index(lowest_location)
        selected_locations[index] = (lowest_location[0], lowest_location[1] - 1)
        current_duration -= 1

      if len(missing_locations) != 0:
        if current_duration == duration:
          lowest_location = max(selected_locations, key=lambda x: x[1])
          index = selected_locations.index(lowest_location)
          selected_locations[index] = (lowest_location[0], lowest_location[1] - 1)
          current_duration -= 1

          selected_locations.append((missing_locations[0], 1))
          location_days[missing_locations[0]] += 1
          current_duration += 1
          missing_locations.pop(0)
        else:
          selected_locations.append((missing_locations[0], 1))
          location_days[missing_locations[0]] += 1
          current_duration += 1
          missing_locations.pop(0)
    return list(filter(lambda x: x[1] > 0, selected_locations))
