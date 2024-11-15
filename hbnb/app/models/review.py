"""Review model module"""
from app.db import db
from app.models.base_model import BaseModel

class Review(BaseModel):
   __tablename__ = 'reviews'

   text = db.Column(db.Text, nullable=False)
   rating = db.Column(db.Integer, nullable=False)
   user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
   place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)

   __table_args__ = (
       db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
   )

   user = db.relationship('User', backref=db.backref('reviews', lazy=True,
                        cascade="all, delete-orphan"))
   place = db.relationship('Place', backref=db.backref('reviews', lazy=True,
                         cascade="all, delete-orphan"))

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.text = kwargs.get('text', '')
       self.rating = int(kwargs.get('rating', 1))
       self.user_id = kwargs.get('user_id', '')
       self.place_id = kwargs.get('place_id', '')
       self.validate()

   def validate(self):
       if not self.text or not self.text.strip():
           raise ValueError("text cannot be empty")
       if not isinstance(self.rating, int) or not 1 <= self.rating <= 5:
           raise ValueError("rating must be between 1 and 5")