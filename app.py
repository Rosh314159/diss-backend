import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from epc_service import get_latest_epc
from feasibility_model import get_feasibility
from recommendation_service import get_similar_houses
from flask_cors import CORS
from data_enricher import enrich_data
from enhanced_search import search_houses
import pandas as pd
from models import db, House
app = Flask(__name__)
# Enable CORS for all routes
CORS(app)
#Initialise DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///houses.db'
db.init_app(app)
with app.app_context():
    db.create_all()  # Ensure tables are created
@app.route('/houses', methods=['GET'])
def get_houses():
    houses = House.query.order_by(func.random()).limit(100).all()  # Get a random sample of 100 houses
    return jsonify([
        {
            'transaction_id': house.transaction_id,
            'price': house.price,
            'ask_price': house.ask_price,
            'predicted_price': house.predicted_price,
            'date_of_transfer': house.date_of_transfer,
            'postcode': house.postcode,
            'property_type': house.property_type,
            'latitude': house.latitude,
            'longitude': house.longitude
        } for house in houses
    ])



@app.route('/fetch-and-enrich', methods=['POST'])
def fetch_epc():
    try:
        # Parse request data
        data = request.json
        postcode = data.get('postcode')
        house_number_or_name = data.get('house_number_or_name')
        # Log the postcode and house number
        print(f"Postcode: {postcode}, House Number/Name: {house_number_or_name}")
        # Validate input
        if not postcode or not house_number_or_name:
            return jsonify({"error": "Postcode and house number/name are required"}), 400

        # Fetch EPC data
        epc_data = get_latest_epc(postcode, house_number_or_name)
        epc_data = enrich_data(epc_data)

        if epc_data.empty:
            return jsonify({"error": "No EPC certificate found for the given address"}), 404

        # Convert DataFrame to dictionary
        epc_dict = epc_data.to_dict(orient='records')[0]
        obj = jsonify({"enriched_data": epc_dict})
        return obj, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
from price_predictor import predict_house_price 

# Endpoint to predict house price
@app.route('/predict-price', methods=['POST'])
def predict_price():
    try:
        # Parse the enriched data from the request
        enriched_data = request.json.get('enriched_data')
        if not enriched_data:
            return jsonify({'status': 'error', 'message': 'Enriched data is required'}), 400

        # Convert to a DataFrame
        enriched_df = pd.DataFrame([enriched_data])

        # Predict the house price
        predicted_price = predict_house_price(enriched_df)

        # Return the predicted price
        response = {
            'status': 'success',
            'predicted_price': predicted_price
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Feasibility assessment endpoint
@app.route('/feasibility', methods=['POST'])
def assess_feasibility():
    try:
        data = request.json
        system_inputs = data.get('system_inputs')
        user_inputs = data.get('user_inputs')

        if not system_inputs or not user_inputs:
            return jsonify({'status': 'error', 'message': 'System inputs and user inputs are required'}), 400

        result = get_feasibility(system_inputs, user_inputs)
        return jsonify({'status': 'success', 'result': result}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/recommendations', methods=['POST'])
def recommend_houses():
    try:
        data = request.json
        house_features = data
        if not house_features:
            return jsonify({'error': 'House features are required for recommendations'}), 400

        recommendations = get_similar_houses(house_features)
        return jsonify({'recommendations': recommendations})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/enhanced_search', methods=['GET'])
def enhanced_search():
    try:
        search_params = request.args.to_dict()
        houses = search_houses(search_params)
        return houses
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port=10000)
