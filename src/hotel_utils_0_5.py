import pandas as pd

def get_hotel_location(hotel, hotel_list):

    # Ensure hotel_list items are in lowercase for consistent comparison
    hotel_list = [hotel_name.lower() for hotel_name in hotel_list]

    # Filter the DataFrame, ensuring case-insensitive matching
    filtered_df = hotel[hotel['Hotels'].isin(hotel_list)]

    # Convert the filtered DataFrame to a dictionary {location: hotel}
    result_dict = dict(zip(filtered_df['Location'], filtered_df['Hotels']))
    
    return result_dict

  
def get_hotel_rates(hotel, hotel_info):
  
    rate_columns = ['Single Half Board Rate','Single Full Board Rate','Single BB Rate']
    # Convert hotel_info dictionary keys and values to lowercase
    hotel_info = {k.lower(): v.lower() for k, v in hotel_info.items()}
   
    location_rate_info = {}

    # Iterate through the hotel_info dictionary
    for location, hotel_name in hotel_info.items():
        # Filter the hotel data based on the hotel name
        hotel_rate_row = hotel[hotel['Hotels'] == hotel_name]
        
        if not hotel_rate_row.empty:
            # Extract the required rate columns for this hotel
            rate_data = hotel_rate_row[rate_columns].to_dict(orient="records")[0]
            location_rate_info[hotel_name] = rate_data
    

    return location_rate_info
