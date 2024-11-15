"""test_amenity_repository.py"""
from app.repositories.amenity_repository import AmenityRepository
from app.models.amenity import Amenity
from app.models.place import Place
import unittest

class TestAmenityRepository(unittest.TestCase):
   def setUp(self):
       self.app = create_app()
       self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
       with self.app.app_context():
           db.create_all()
           self.repo = AmenityRepository()

   def tearDown(self):
       with self.app.app_context():
           db.session.remove()
           db.drop_all()

   def test_create_amenity(self):
       with self.app.app_context():
           amenity = Amenity(name='WiFi')
           saved = self.repo.add(amenity)
           self.assertEqual(saved.name, 'WiFi')

   def test_get_by_name(self):
       with self.app.app_context():
           amenity = Amenity(name='Pool')
           self.repo.add(amenity)
           found = self.repo.get_by_name('Pool')
           self.assertEqual(found.name, 'Pool')

   def test_get_by_place(self):
       with self.app.app_context():
           user = User(email='test@test.com', password='test123',
                      first_name='Test', last_name='User')
           db.session.add(user)
           
           place = Place(title='Test Place', price=100,
                        owner_id=user.id)
           amenity = Amenity(name='WiFi')
           
           db.session.add(place)
           db.session.add(amenity)
           place.amenities.append(amenity)
           db.session.commit()

           amenities = self.repo.get_by_place(place.id)
           self.assertEqual(len(amenities), 1)
           self.assertEqual(amenities[0].name, 'WiFi')
