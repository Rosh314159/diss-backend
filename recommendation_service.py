from sklearn.metrics.pairwise import cosine_similarity
from models import House, db
import pandas as pd

def get_similar_houses(house_features):
    try:
        # Extract target features
        target_price = house_features.get('predicted_price')
        target_latitude = house_features.get('latitude')
        target_longitude = house_features.get('longitude')
        
        # Fetch houses from the database
        houses = House.query.limit(100).all()

        full_house_data = [house.__dict__ for house in houses]
        for house in full_house_data:
            house.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state if present
        # Convert to DataFrame
        similarity_data = [{
            'price': house.price,
            'latitude': house.latitude,
            'longitude': house.longitude
        } for house in houses]

        similarity_df = pd.DataFrame(similarity_data)

        # Include target house
        target_house = pd.DataFrame([{
            'price': target_price,
            'latitude': target_latitude,
            'longitude': target_longitude
        }])

        # Combine and compute cosine similarity
        combined_df = pd.concat([target_house, similarity_df])
        similarity_matrix = cosine_similarity(combined_df)

        # Get similarity scores for the target house
        similarity_scores = similarity_matrix[0][1:]  # Exclude the target house itself

        # Add similarity scores to full house data
        for idx, house in enumerate(full_house_data):
            house['similarity'] = similarity_scores[idx]

        # Sort houses by similarity and return top 5
        recommended_houses = sorted(full_house_data, key=lambda x: x['similarity'], reverse=True)[:5]

        return recommended_houses
    
    except Exception as e:
        return {'error': str(e)}
