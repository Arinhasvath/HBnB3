class TestPlaceAPI(unittest.TestCase):
   def setUp(self):
       self.app = create_app()
       self.client = self.app.test_client()
       with self.app.app_context():
           db.create_all()
           self.user = User(
               email='owner@test.com',
               password='test123',
               first_name='Owner',
               last_name='User'
           )
           db.session.add(self.user)
           db.session.commit()
           self.user_id = self.user.id

   def test_create_place(self):
       response = self.client.post('/api/v1/places', json={
           'title': 'Beach House',
           'description': 'Beautiful beachfront property',
           'price': 150.0,
           'owner_id': self.user_id
       })
       self.assertEqual(response.status_code, 201)
       data = json.loads(response.data)
       self.assertEqual(data['title'], 'Beach House')
