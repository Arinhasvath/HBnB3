"""test_models_integration.py: Integration tests for the models."""
import unittest
from app import create_app, db
from app.models import User, Place, Review, Amenity

class TestModelsIntegration(unittest.TestCase):
   def setUp(self):
       self.app = create_app()
       self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
       with self.app.app_context():
           db.create_all()
           self.user = User(
               email='test@test.com',
               password='test123',
               first_name='Test',
               last_name='User'
           )
           db.session.add(self.user)
           db.session.commit()

   def test_user_place_relationship(self):
       with self.app.app_context():
           place = Place(
               title='Test Place',
               description='Description',
               price=100.0,
               owner_id=self.user.id
           )
           db.session.add(place)
           db.session.commit()
           
           self.assertEqual(len(self.user.places), 1)
           self.assertEqual(place.owner.id, self.user.id)

   def test_place_reviews(self):
       with self.app.app_context():
           place = Place(title='Test Place', price=100, owner_id=self.user.id)
           db.session.add(place)
           
           review = Review(
               text='Great place!',
               rating=5,
               user_id=self.user.id,
               place_id=place.id
           )
           db.session.add(review)
           db.session.commit()
           
           self.assertEqual(len(place.reviews), 1)
           self.assertEqual(review.user.id, self.user.id)

   def test_place_amenities(self):
       with self.app.app_context():
           place = Place(title='Test Place', price=100, owner_id=self.user.id)
           amenity = Amenity(name='WiFi')
           
           db.session.add(place)
           db.session.add(amenity)
           place.amenities.append(amenity)
           db.session.commit()
           
           self.assertEqual(len(place.amenities), 1)
           self.assertEqual(len(amenity.places), 1)

   def tearDown(self):
       with self.app.app_context():
           db.session.remove()
           db.drop_all()
