"""place model module."""
from app.db import db
from app.models.base_model import BaseModel
from app.models.association_tables import place_amenities

class Place(BaseModel):
   __tablename__ = 'places'
   
   title = db.Column(db.String(255), nullable=False)
   description = db.Column(db.String(1024))
   price = db.Column(db.Float, nullable=False)
   latitude = db.Column(db.Float)
   longitude = db.Column(db.Float)
   owner_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

   amenities = db.relationship('Amenity', secondary=place_amenities,
                             backref=db.backref('places', lazy=True))
   owner = db.relationship('User', backref=db.backref('places', lazy=True, 
                         cascade="all, delete-orphan"))

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.title = kwargs.get('title', '')
       self.description = kwargs.get('description', '')
       self.price = float(kwargs.get('price', 0))
       self.latitude = kwargs.get('latitude')
       self.longitude = kwargs.get('longitude')
       self.owner_id = kwargs.get('owner_id')
       self.validate()

   def validate(self):
       if not self.title or not self.title.strip():
           raise ValueError("Title cannot be empty")
       if self.description and not self.description.strip():
           raise ValueError("Description cannot be empty if provided")
       if not isinstance(self.price, (int, float)) or self.price < 0:
           raise ValueError("Price must be a positive number")
       if self.latitude and not isinstance(self.latitude, (int, float)):
           raise ValueError("Invalid latitude")
       if self.longitude and not isinstance(self.longitude, (int, float)):
           raise ValueError("Invalid longitude")

