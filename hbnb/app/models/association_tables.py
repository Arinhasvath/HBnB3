""" association_tables.py"""
from app.db import db

place_amenities = db.Table('place_amenities',
   db.Column('place_id', db.String(36), 
             db.ForeignKey('places.id', ondelete='CASCADE'), 
             primary_key=True),
   db.Column('amenity_id', db.String(36), 
             db.ForeignKey('amenities.id', ondelete='CASCADE'), 
             primary_key=True)
)