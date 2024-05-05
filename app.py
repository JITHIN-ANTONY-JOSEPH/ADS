from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import ipaddress
import pandas as pd

app = Flask(__name__)

# Load your trained model
model = pickle.load(open('lgb_model.pkl', 'rb'))
# Load the saved encoders
with open('encoders.pkl', 'rb') as file:
    encoders = pickle.load(file)

# Define column names
column_names = ['start', 'end', 'country_code', 'country', 'region', 'city', 'lat', 'long']
def ip_to_int(ip):
    try:
        return int(ipaddress.ip_address(ip))
    except ValueError:
        return None  # Handle the case where the IP address is invalid

# Read the CSV file with specified column names
ip_map = pd.read_csv('IP2LOCATION-LITE-DB5.csv', names=column_names)
# Convert IP range start and end to integers
ip_map['start_int'] = ip_map['start'].apply(ip_to_int)
ip_map['end_int'] = ip_map['end'].apply(ip_to_int)

# Create IntervalIndex from these ranges
ip_map['ip_range'] = pd.IntervalIndex.from_arrays(ip_map['start_int'], ip_map['end_int'], closed='both')
ip_map.set_index('ip_range', inplace=True)

# Load the wallet to age mapping
wallet_to_age = pd.read_csv('Age_Mapping.csv')

@app.route('/')
def index():
    return render_template('index.html')  # Ensure your HTML file is named index.html

from flask import Flask, request, jsonify


    
def lookup_geo_data(ip_num):
    try:
        record = ip_map.loc[ip_num]
        return {
            'country': record['country'],
            'city': record['city'],
            'region': record['region']
        }
    except KeyError:
        return {
            'country': None,
            'city': None,
            'region': None
        }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        ip_number = ip_to_int(data['ip_address'])  # Convert IP address to number
        
        if ip_number is None:
            raise ValueError("Invalid IP address")
        
        # Lookup geo data based on the numerical IP
        geo_data = lookup_geo_data(ip_number)

        if not geo_data['country']:  # Check if geolocation data was successfully retrieved
            raise ValueError("Geolocation data not found for the IP address")
        
        # Lookup Adjusted Account Age from the wallet number
        wallet_from = data['wallet_from']
        filtered_data = wallet_to_age[wallet_to_age['wallet_number_from'] == int(wallet_from)]
        #wallet_to_age.info()
        if not filtered_data.empty:
            adjusted_account_age = filtered_data['Adjusted Account Age'].iloc[0]
        else:
            raise ValueError("Wallet number not found in age mapping")

        # Collect data from form and other sources
        features = {
            'ip_number': ip_number,
            'wallet_to': data['wallet_to'],
            'region': geo_data['region'],
            'adjusted_account_age': adjusted_account_age,
            'browser_environment': data['browser_env'],
            'wallet_from': data['wallet_from'],
            'business_type_class': data['business_type_class'],
            'city': geo_data['city'],
            'trx_type': data['trx_type'],
            'country': geo_data['country'],
            'amount': data['amount']
        }
        #print(features)
        #print(encoders)
        # Encode features using label encoders
        encoded_features = []
        for feature, value in features.items():
            if feature in encoders:
                # Encode the feature
                encoded_feature = encoders[feature].transform([value])[0]
                encoded_features.append(encoded_feature)
            else:
                # Use the numerical value directly (assuming it's already suitable for model input)
                encoded_features.append(float(value))
        print(encoded_features)

        #features = np.array([[data['amount'], ip_number, data['wallet_to'], geo_data['region'], adjusted_account_age, data['browser_env'], data['wallet_from'], data['business_type_class'], geo_data['city'], data['trx_type'], geo_data['country']]])
        #print(features)
        
        prediction = model.predict([encoded_features])
        predicted_class = (prediction >= 0.5).astype(int)
        result = 'Anomaly' if predicted_class == 1 else 'Not Anomaly'
        print(prediction)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})
        
if __name__ == '__main__':
    app.run(debug=True)