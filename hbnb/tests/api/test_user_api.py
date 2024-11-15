import unittest
import json
from app import create_app, db

class TestUserAPI(unittest.TestCase):
   def setUp(self):
       self.app = create_app()
       self.app.config['TESTING'] = True
       self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
       self.client = self.app.test_client()
       with self.app.app_context():
           db.create_all()

   def test_create_user(self):
       response = self.client.post('/api/v1/users', json={
           'email': 'test@test.com',
           'password': 'test123',
           'first_name': 'Test',
           'last_name': 'User'
       })
       self.assertEqual(response.status_code, 201)
       data = json.loads(response.data)
       self.assertEqual(data['email'], 'test@test.com')