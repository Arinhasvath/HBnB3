"""Amenity model module"""
from app.db import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
   __tablename__ = 'amenities'
   
   name = db.Column(db.String(128), nullable=False, unique=True)

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.name = kwargs.get('name', '')
       self.validate()

   def validate(self):
       if not self.name or not self.name.strip():
           raise ValueError("name cannot be empty")

   def to_dict(self):
       return {
           'id': self.id,
           'name': self.name,
           'created_at': self.created_at.isoformat(),
           'updated_at': self.updated_at.isoformat()
       }