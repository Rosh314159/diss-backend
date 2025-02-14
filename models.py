from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    ask_price = db.Column(db.Integer, nullable=False)
    predicted_price = db.Column(db.Integer, nullable=False)
    date_of_transfer = db.Column(db.String(50))
    postcode = db.Column(db.String(20))
    property_type = db.Column(db.String(10))
    new_build = db.Column(db.String(5))
    duration = db.Column(db.String(20))
    paon = db.Column(db.String(200))
    saon = db.Column(db.String(200))
    street = db.Column(db.String(200))
    locality = db.Column(db.String(200))
    town_city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    county = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    nearest_primary_school_distance = db.Column(db.Float)
    nearest_secondary_school_distance = db.Column(db.Float)
    nearest_train_station_distance = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<House {self.transaction_id}>"

