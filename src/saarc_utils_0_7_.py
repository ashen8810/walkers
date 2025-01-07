import pandas as pd

def get_saarc_entrance_fees(activities, saarc_fees):
    # Convert all activity names in the input to lowercase
    activities_lower = {location: [activity.lower() for activity in acts] for location, acts in activities.items()}
     
    # Prepare a list to store the results
    all_activities_fees = []
    
    # Iterate through each location and their activities
    for location, acts in activities_lower.items():
        for activity in acts:
            # Check if the activity is in the SAARC fee table
            if activity in saarc_fees['Activity'].values:
                # Fetch the entrance fees for adult and child
                fee_row = saarc_fees[saarc_fees['Activity'] == activity].iloc[0]
                fee_info = {
                    "activity": activity,
                    "adultFee": f"{fee_row['SAARC entrance fees per adults - USD']} $",
                    "childFee": f"{fee_row['SAARC entrance fees per child (5-11.99 years)']} $"
                }
                # Add the activity's fee information to the result list
                all_activities_fees.append(fee_info)
    
    # Return the list of fees for activities in the SAARC fee table
    return {"fees": all_activities_fees}