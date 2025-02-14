import pandas as pd
from sklearn.preprocessing import LabelEncoder
from joblib import load  # To load your saved model

loaded = False
DATA_PATH = 'C:\\Users\\rosh0\\cs\\HomeIQ\\backend\\data'
def load_models():
# Load the saved model, label encoders and dictionary of local authority average prices
    print("loading models")
    global model, label_encoder_property_type, average_price_per_local_authority
    model = load(f'{DATA_PATH}\\house_price_model.joblib')
    label_encoder_property_type = load(f'{DATA_PATH}\\property_type_encoder.joblib') 
    average_price_per_local_authority = load(f'{DATA_PATH}\\average_price_per_local_authority.joblib')
    global loaded
    loaded = True
    print("Finished loading models")
def predict_house_price(data):
    """
    Predicts house price using the enriched data.
    
    Parameters:
    epc_df (pd.DataFrame): The enriched DataFrame.

    Returns:
    float: Predicted house price.
    """ 
    if not loaded:
        load_models()

    # Define relevant columns for the model
    relevant_columns = [
        'age_in_years', 'postcode', 'property_type', 'local-authority-label', 
        'total-floor-area', 'number-habitable-rooms', 'number-open-fireplaces',
        'nearest_primary_school_distance', 'nearest_secondary_school_distance', 
        'nearest_primary_school_outstanding', 'nearest_secondary_school_outstanding', 
        'nearest_shop_distance', 'nearest_train_station_distance', 'nearest_bus_stop_distance'
    ]
    print("h")
    # Select relevant columns
    data = data[relevant_columns]
    X = data.copy()
    
    
    X['average_price_in_area'] = X['local-authority-label'].map(average_price_per_local_authority)
    print(X.columns)
    # Encode categorical features
    X['property_type_encoded'] = label_encoder_property_type.transform(X['property_type'])
    print(X.columns)
    # Drop original categorical columns
    X = X.drop(columns=['postcode', 'local-authority-label', 'property_type', 'number-habitable-rooms'])
    print(X.columns)
    # Predict house price
    predicted_price = model.predict(X)
    print("f")
    return predicted_price[0]
