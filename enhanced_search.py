from models import House, db
from flask import request, jsonify

def search_houses(search_params):
    try:
        query = House.query

        # Extract query parameters
        price_min = int(search_params['priceMin'])
        price_max = int(search_params['priceMax'])
        postcode = search_params['postcode']
        property_type = search_params['propertyType']
        town_city = search_params['townCity']

        # Apply filters based on query parameters
        if price_min is not None:
            query = query.filter(House.ask_price >= price_min)
        if price_max is not None:
            query = query.filter(House.ask_price <= price_max)
        if postcode is not None:
            query = query.filter(House.postcode.like(f"%{postcode}%"))
        if property_type is not None:
            query = query.filter(House.property_type == property_type)
        if town_city is not None:
            query = query.filter(House.town_city.like(f"%{town_city}%"))

        # Execute query and fetch results
        houses = query.all()

        # Convert query results to list of dictionaries
        house_list = [
            {
                'transaction_id': house.transaction_id,
                'price': house.price,
                'ask_price': house.ask_price,
                'predicted_price': house.predicted_price,
                'postcode': house.postcode,
                'property_type': house.property_type,
                'paon': house.paon,
                'street': house.street,
                'town_city': house.town_city,
                'latitude': house.latitude,
                'longitude': house.longitude,
            }
            for house in houses
        ]

        return jsonify(house_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
