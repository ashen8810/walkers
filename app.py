from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from numpy import double, single
import pandas as pd
import json
from pipeline import main
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the CSV files into DataFrames
try:
    hotels_df = pd.read_csv('hotels.csv', encoding='ISO-8859-1')
    itenaries_df = pd.read_csv('iternary 1(in).csv', encoding='ISO-8859-1')
except Exception as e:
    print(f"Error loading CSV files: {e}")
    hotels_df = pd.DataFrame()  # Fallback to an empty DataFrame
    itenaries_df = pd.DataFrame()

@app.route('/locations', methods=['GET'])
def get_locations():
    """
    Endpoint to retrieve all unique locations from the itenaries table.
    """
    try:
        locations = itenaries_df['location'].dropna().unique().tolist()
        locations = [word.lower().capitalize() for word in locations]
        return jsonify(locations)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch locations: {str(e)}"}), 500

@app.route('/star', methods=['POST'])
def get_star_rating():
    """
    Endpoint to retrieve star ratings based on selected locations.
    """
    try:
        data = request.get_json()
        selected_locations = data.get('locations', [])
        
        selected_locations = [word.lower().capitalize() for word in selected_locations]

        # Filter hotels based on selected locations
        filtered_hotels = hotels_df[hotels_df['Location'].isin(selected_locations)]
        filtered_hotels = [word.lower().capitalize() for word in filtered_hotels]

        
        # Get unique star ratings
        star_rating = filtered_hotels['star'].dropna().unique().tolist()
        return jsonify(star_rating)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch star ratings: {str(e)}"}), 500

@app.route('/hotels', methods=['GET'])
def get_hotels():
    """
    Endpoint to retrieve hotel names based on selected locations
    """
    try:
        # Extract hotel names
        hotels_df['Hotels'] = hotels_df['Hotels'].str.title()
        hotels_df['Location'] = hotels_df['Location'].str.title()
        hotel_names = hotels_df[['Hotels',"Location","star"]].dropna().to_json(orient='records', lines=False)
        
        print(hotel_names)
        return jsonify(hotel_names)
    except Exception as e:
        print(e)
        return jsonify({"error": f"Failed to fetch hotels: {str(e)}"}), 500
    

@app.route('/report', methods=['POST'])
def get_report():
    print(request.get_json())
    try:
      from datetime import datetime, timedelta
      data = request.get_json()
      locations = data.get('locations', [])
      start_date = data.get('startDate')
      date_obj = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
      start_date = (date_obj + timedelta(days=1)).isoformat() + "Z"
      end_date = data.get('endDate')
      duration = data.get('duration')
      pax_size = data.get('paxSize')
      hotels = data.get('hotels',[])
      # star = data.get("category")
      # budget = data.get("budget")
      # distance = data.get("distance")
      # double = data.get("double")
      # single = data.get("single")
      # triple = data.get("triple")

      locations = [i.lower() for i in locations]
      if "colombo" not in locations:
          duration["days"] = int(duration["days"])-1
          
      hotels = [i.split("-")[0] for i in hotels]
 
      def capitalize_values(data):
          if isinstance(data, dict):
              return {k: capitalize_values(v) for k, v in data.items()}
          elif isinstance(data, list):
              return [capitalize_values(item) for item in data]
          elif isinstance(data, str):
              return data.title()  
          else:
              return data

      reports = main.generate_trip_details(locations, hotels, start_date.split("T")[0],end_date.split("T")[0],duration['days'],pax_size)
      reports = capitalize_values(reports)
      print(reports)
      # reports = { "trips": [{'startDate': '2024-12-01', 'endDate': '2024-12-03', 'location': 'kandy', 'hotel': 'devon', 'activities': ['pinnawela elephant orphanage', 'cultural dance show ', 'kandy temple'], 'duration_of_stay': 3, 'rates': {'Single Half Board Rate': 47.0, 'Single Full Board Rate': 57.0, 'Single BB Rate': 37.0}}, {'startDate': '2024-12-04', 'endDate': '2024-12-07', 'location': 'colombo', 'hotel': 'ocean edge', 'activities': ['colombo city tour & shopping ', 'lotus tower', 'departure airport drop'], 'duration_of_stay': 4, 'rates': {'Single Half Board Rate': 55.0, 'Single Full Board Rate': 65.0, 'Single BB Rate': 45.0}}], 'transport_type': 'Coach', 'transport_cost': 3789.5, 'fees': [{'activity': 'pinnawela elephant orphanage', 'adultFee': '10 $', 'childFee': '0 $'}]}
      return jsonify({"report": reports})
      
    except Exception as e:
      print(e)
      return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the Flask app: {e}")
