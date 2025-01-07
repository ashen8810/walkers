import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import timedelta
import pandas as pd
from conf.conf_script import get_conf
from src.utilities_0_1 import load_itinerary, load_hotels, load_transport_data, load_saarc_fees
from src.location_utils_0_2 import find_best_tour_with_days
from src.distance_utils_0_3 import find_shortest_path
from src.hotel_utils_0_5 import get_hotel_location, get_hotel_rates
from src.transport_utils_0_6 import get_transport_cost
from src.saarc_utils_0_7_ import get_saarc_entrance_fees
from src.activities_utils_0_4 import get_activities_by_locations

def generate_trip_details(locations, hotel_list, start_date, end_date, duration, pax_size):
    trip_details = []
    total_days = 0
    current_date = pd.to_datetime(start_date)

    # Get configuration from conf_script
    config = get_conf()

    # Load data using the appropriate functions from utilities_0_1
    iternary = load_itinerary(config["paths"]["itinerary_data"])
    hotel = load_hotels(config["paths"]["hotel_data"])
    transport_data = load_transport_data(config["paths"]["transport_data"])
    saarc_fees = load_saarc_fees(config["paths"]["saarc_fees_data"])

    selected_locations = find_best_tour_with_days(iternary, locations, duration)
    path, distance = find_shortest_path(selected_locations)
    activities = get_activities_by_locations(iternary,path)
    hotel_info = get_hotel_location(hotel, hotel_list)
    transport_cost = get_transport_cost(transport_data,pax_size,distance)
    fees_data = get_saarc_entrance_fees(activities,saarc_fees)
    selected_locations_dict = dict(selected_locations)

    current_start_date = pd.to_datetime(start_date)

    for location in path:
        # Find the duration of stay for the current location
        days = selected_locations_dict.get(location, 1)
        # Calculate the end date for this location
        location_end_date = current_start_date + timedelta(days=days - 1)

        # Get activities for the location
        activities = get_activities_by_locations(iternary, [location])

        # Get hotel rates for the location
        rates = get_hotel_rates(hotel, hotel_info)
        print("*********************")
        print(hotel_info.get(location, ""))
        # Add trip details to the list
        trip_details.append({
            "startDate": current_start_date.strftime("%Y-%m-%d"),
            "endDate": location_end_date.strftime("%Y-%m-%d"),
            "location": location,
            "hotel": hotel_info.get(location, ""),
            "activities": activities.get(location, []),
            "duration_of_stay": days,
            "rates": rates.get(hotel_info.get(location.strip(), ""), [])
        })

        # Update start date for the next location
        current_start_date = location_end_date + timedelta(days=1)

    # Get transport details (type and cost)
    transport_type = transport_cost["transport_type"]
    transport_cost_value = transport_cost["transport_cost"]

    # Return the trip plan dictionary
    return {
        "trips": trip_details,
        "transport_type": transport_type,
        "transport_cost": transport_cost_value,
        "fees": fees_data["fees"]
    }
