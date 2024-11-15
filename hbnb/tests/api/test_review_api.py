class TestReviewAPI(unittest.TestCase):
   def setUp(self):
       self.app = create_app()
       self.client = self.app.test_client()
       with self.app.app_context():
           db.create_all()
           
           # Create test user and place
           self.user = User(email='reviewer@test.com', password='test123',
                          first_name='Reviewer', last_name='User')
           db.session.add(self.user)
           
           self.place = Place(title='Test Place', price=100,
                            owner_id=self.user.id)
           db.session.add(self.place)
           db.session.commit()

   def test_create_review(self):
       response = self.client.post('/api/v1/reviews', json={
           'text': 'Great stay!',
           'rating': 5,
           'user_id': self.user.id,
           'place_id': self.place.id
       })
       self.assertEqual(response.status_code, 201)
       data = json.loads(response.data)
       self.assertEqual(data['rating'], 5)