def get_conf():
    """
    Load all needed configurations to run the jobs and pipelines
    """
    conf = {
        "paths": {
            "itinerary_data": "iternary 1(in).csv",
            "hotel_data": "hotels.csv",
            "transport_data": "transport cost.csv",
            "saarc_fees_data": "SAARC entrance fee.csv"
        }
    }
    
    return conf
