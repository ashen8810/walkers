import pandas as pd

def get_activities_by_locations(itinerary, path):

    # Drop duplicates and missing values
    itinerary = itinerary.drop_duplicates(subset=['location', 'activity'])
    itinerary = itinerary.dropna(subset=['location', 'activity'])
    
    # Convert path to lowercase
    path = [p.lower() for p in path]
    
    # Group activities by location
    grouped_activities = itinerary.groupby("location")["activity"].apply(list)
    
    # Filter to include only locations in the path
    grouped_activities = grouped_activities[grouped_activities.index.isin(path)]
    
    # Create a dictionary with up to 3 activities per location
    location_dict = {}
    for location, activities in grouped_activities.items():
        if location == "colombo":
            # Remove 'departure airport drop' if it already exists
            activities = [activity for activity in activities if activity != "departure airport drop"]
            # Add up to two activities and ensure 'departure airport drop' is the last one
            location_dict[location] = activities[:2] + ["departure airport drop"]
        else:
            location_dict[location] = activities[:3]
    
    return location_dict

