from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/timeseries', methods=['POST'])
def handle_timeseries():
    if request.is_json:
        try:
            data = request.get_json()  # Get JSON data from the request
            time_series_data = data.get('time_series', [])

            date = '2023-06-01'
            
            timestamp1 = pd.Timestamp(date)
            timestamp2 = pd.Timestamp(time_series_data)
            with open('./sarimax_model without exog.pkl', 'rb') as f:
                loaded_model = pickle.load(f)
            
            predictions = loaded_model.get_prediction(start=timestamp1, end=timestamp2,dynamic=True,step=30)

            predicted_values = predictions.predicted_mean
            pred = predicted_values

            response = {
                'status': 'success',
                'message': pred.to_json(orient='records')
            }
            return jsonify(response), 200
        except Exception as e:
            error_response = {
                'status': 'error',
                'message': 'An error occurred while processing the time series data',
                'error_details': str(e)
            }
            return jsonify(error_response), 500
    else:
        # Return error response if the request does not contain JSON data
        return jsonify({'error': 'Request must contain JSON data'}), 400
@app.route('/timeserieswithexog', methods=['POST'])
def handle_timeseries_with_exog():
    if request.is_json:
        try:
            data = request.get_json()  # Get JSON data from the request
            time_series_data = data.get('date')
            exog_rainfall = data.get('rainfall')
            exog_holiday = data.get('holiday')
            print(time_series_data)
            print(type(exog_rainfall))
            print(exog_holiday)
            date = '2023-06-01'

            dates = pd.date_range(start=date, end = time_series_data) 
            if len(dates) != len(exog_rainfall) or len(dates) != len(exog_holiday):
                return jsonify({'error': 'Mismatch Lengths'})
            exog_test = pd.DataFrame({"Rainfall": exog_rainfall, "Holiday": exog_holiday}, index=dates)



            with open('./sarimax_model.pkl', 'rb') as f:
                loaded_model = pickle.load(f)
            timestamp1 = pd.Timestamp(date)
            timestamp2 = pd.Timestamp(time_series_data)
            
            predictions = loaded_model.get_prediction(start=timestamp1, end=timestamp2,dynamic=True,step=30,exog  = exog_test)
            predicted_values = predictions.predicted_mean
            pred = predicted_values
            print(pred)
            response = {
                'status': 'success',
                'message': pred.to_json(orient='records')
            }
            return jsonify(response), 200
        except Exception as e:
            # Handle any exceptions that occur during processing
            error_response = {
                'status': 'error',
                'message': 'An error occurred while processing the time series data',
                'error_details': str(e)
            }
            return jsonify(error_response), 500
    else:
        return jsonify({'error': 'Request must contain JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
