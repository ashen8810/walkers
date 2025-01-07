import pandas as pd

def get_transport_cost(transport, pax_size, distance):
   
    # Filter the transport options based on the pax_size
    filtered_transport = transport[transport['pax size'] >= pax_size]
    
    # If no suitable transport options are found
    if filtered_transport.empty:
        return {"transport_type": "No suitable transport found", "transport_cost": "N/A"}
    
    # Calculate the transport cost based on the price per km
    transport_cost = {}
    
    for _, row in filtered_transport.iterrows():
        car_type = row['Car Type']
        price_per_km = row['Price per 1km']
        
        # Calculate the transport cost for the given distance
        total_cost = price_per_km * distance
        
        # Store the result in the dictionary
        transport_cost[car_type] = total_cost

    # If multiple transport types are available, select the one with the minimum cost
    min_cost_transport = min(transport_cost, key=transport_cost.get)
    return {
    "transport_type": min_cost_transport,
    "transport_cost": round(transport_cost[min_cost_transport], 2)
}
