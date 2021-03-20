from app import app, db
import enum


class PropertyType(enum.Enum):
    HOUSE = "House"
    APARTMENT = 'Apartment'


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    bedroom_count = db.Column(db.Integer)
    bathroom_count = db.Column(db.Integer)
    location = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2, asdecimal=False))
    type = db.Column(db.Enum(PropertyType))
    description = db.Column(db.String(1500))
    photo_path = db.Column(db.String(255))

    def __init__(self, title, bedroom_count, bathroom_count, location, price, type, description, photo_path) -> None:
        super().__init__()
        self.title = title
        self.bedroom_count = bedroom_count
        self.bathroom_count = bathroom_count
        self.location = location
        self.price = price
        self.type = type
        self.description = description
        self.photo_path = photo_path


db.create_all()
