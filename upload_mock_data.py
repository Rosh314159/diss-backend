import pandas as pd
from app import app, db  # Import app to create context
from models import House
import sys

def upload_csv(file_path):
    try:
        df = pd.read_csv(file_path, low_memory=False)

        # Fix the FutureWarning issue
        for column in df.select_dtypes(include=['float64']).columns:
            df[column] = df[column].astype('float64').fillna(0)

        for column in df.select_dtypes(include=['object']).columns:
            df[column] = df[column].fillna("")

        batch_size = 500  
        records = []

        with app.app_context():  # Wrap everything in app.app_context()
            for _, row in df.iterrows():
                house = House(
                    transaction_id=row['transaction_id'],
                    price=int(row['price']),
                    ask_price=int(row['ask_price']),
                    predicted_price=int(row['predicted_price']),
                    date_of_transfer=row['date_of_transfer'],
                    postcode=row['postcode'],
                    property_type=row['property_type'],
                    new_build=row['new_build'],
                    duration=row['duration'],
                    paon=row['paon'],
                    saon=row['saon'],
                    street=row['street'],
                    locality=row['locality'],
                    town_city=row['town_city'],
                    district=row['district'],
                    county=row['county'],
                    latitude=row['latitude'] if row['latitude'] else None,
                    longitude=row['longitude'] if row['longitude'] else None,
                    nearest_primary_school_distance=row['nearest_primary_school_distance'] if row['nearest_primary_school_distance'] else None,
                    nearest_secondary_school_distance=row['nearest_secondary_school_distance'] if row['nearest_secondary_school_distance'] else None,
                    nearest_train_station_distance=row['nearest_train_station_distance'] if row['nearest_train_station_distance'] else None,
                )
                records.append(house)

                if len(records) >= batch_size:
                    db.session.bulk_save_objects(records)  
                    db.session.commit()
                    records = []

            if records:
                db.session.bulk_save_objects(records)
                db.session.commit()

            print("✅ CSV data uploaded successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_csv.py <path_to_csv>")
    else:
        upload_csv(sys.argv[1])

