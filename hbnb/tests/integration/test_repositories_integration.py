"""test_repositories_integration.py"""
class TestRepositoriesIntegration(unittest.TestCase):
   def setUp(self):
       self.app = create_app()
       self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
       with self.app.app_context():
           db.create_all()
           
           self.user_repo = UserRepository()
           self.place_repo = PlaceRepository()
           self.review_repo = ReviewRepository()
           self.amenity_repo = AmenityRepository()

   def test_complete_booking_flow(self):
       with self.app.app_context():
           # Create user
           user = User(email='guest@test.com', password='test123',
                      first_name='Guest', last_name='User')
           self.user_repo.add(user)

           # Create place with amenities
           place = Place(title='Luxury Villa', price=200, owner_id=user.id)
           self.place_repo.add(place)

           wifi = Amenity(name='WiFi')
           pool = Amenity(name='Pool')
           self.amenity_repo.add(wifi)
           self.amenity_repo.add(pool)
           
           place.amenities.extend([wifi, pool])
           db.session.commit()

           # Add review
           review = Review(text='Amazing stay!', rating=5,
                         user_id=user.id, place_id=place.id)
           self.review_repo.add(review)

           # Verify relationships
           saved_place = self.place_repo.get(place.id)
           self.assertEqual(len(saved_place.amenities), 2)
           self.assertEqual(len(saved_place.reviews), 1)
           self.assertEqual(saved_place.owner.id, user.id)

   def tearDown(self):
       with self.app.app_context():
           db.session.remove()
           db.drop_all()