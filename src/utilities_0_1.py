import pandas as pd

# Load itinerary df
def load_itinerary(file_path):
    """Load the itinerary file and preprocess location data."""
    try:
        # Attempt to read the file
        itinerary = pd.read_csv(file_path, encoding='ISO-8859-1')
        
        # Ensure required columns exist
        if 'location' not in itinerary.columns or 'activity' not in itinerary.columns:
            raise KeyError("The required columns 'location' and 'activity' are missing in the file.")
        
        # Preprocess data
        itinerary['location'] = itinerary['location'].str.lower()
        itinerary['activity'] = itinerary['activity'].str.lower()
        
        return itinerary
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty. Please provide a valid file.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Return None if an error occurs
    return None


# Load hotel df
def load_hotels(file_path):
    """Load the hotels file and preprocess hotel and location data."""
    try:
        hotel = pd.read_csv(file_path, encoding='ISO-8859-1')
        
        # Ensure required columns exist
        if 'Hotels' not in hotel.columns or 'Location' not in hotel.columns:
            raise KeyError("The required columns 'Hotels' and 'Location' are missing in the file.")
        
        hotel['Hotels'] = hotel['Hotels'].str.lower()
        hotel['Location'] = hotel['Location'].str.lower()
        
        return hotel
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty. Please provide a valid file.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None


# load transport_data df
def load_transport_data(file_path):
    """Load the transport data file and remove rows with null values."""
    try:
        # Load the CSV file
        transport_data = pd.read_csv(file_path, encoding='ISO-8859-1')
        
        # Remove rows with null values in any column
        transport_data = transport_data.dropna()
        
        return transport_data
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty. Please provide a valid file.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None



# Load aarc_fees df
def load_saarc_fees(file_path):
    """Load the SAARC fees file and preprocess activity data."""
    try:
        saarc_fees = pd.read_csv(file_path, encoding='ISO-8859-1')
        
        # Ensure required columns exist
        if 'Activity' not in saarc_fees.columns:
            raise KeyError("The required column 'Activity' is missing in the file.")
        
        saarc_fees['Activity'] = saarc_fees['Activity'].str.lower()
        
        return saarc_fees
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty. Please provide a valid file.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

    