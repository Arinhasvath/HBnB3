"""
association_tables.py
This module defines association tables for many-to-many relationships.
"""

from app import db

# Association table for many-to-many relationship between Place and Amenity
place_amenities = db.Table(
    "place_amenities",
    db.Column(
        "place_id", db.Integer, db.ForeignKey("places.id"), primary_key=True
    ),
    db.Column(
        "amenity_id",
        db.Integer,
        db.ForeignKey("amenities.id"),
        primary_key=True,
    ),
    extend_existing=True,  # Ensures compatibility if the table already exists
)
