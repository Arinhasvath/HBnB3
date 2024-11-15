"""Test suite for admin endpoints."""
import unittest
import json
from app import create_app
from app.db import db
from app.models import User, Place, Review, Amenity
from flask_jwt_extended import create_access_token

class TestAdminEndpoints(unittest.TestCase):
    """Test cases for admin endpoints."""

    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create admin user
        self.admin = User(
            email='admin@test.com',
            first_name='Admin',
            last_name='Test',
            is_admin=True
        )
        self.admin.set_password('admin123')
        db.session.add(self.admin)
        db.session.commit()

        # Create admin token
        with self.app.app_context():
            self.admin_token = create_access_token(identity={
                'id': self.admin.id,
                'is_admin': True
            })
            self.headers = {
                'Authorization': f'Bearer {self.admin_token}',
                'Content-Type': 'application/json'
            }

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_admin_create_user(self):
        """Test admin creating a new user."""
        response = self.client.post('/api/v1/users/', 
            headers=self.headers,
            json={
                'email': 'new@test.com',
                'first_name': 'New',
                'last_name': 'User',
                'password': 'pass123'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'new@test.com')

    def test_admin_manage_amenity(self):
        """Test admin managing amenities."""
        # Create amenity
        response = self.client.post('/api/v1/amenities/', 
            headers=self.headers,
            json={'name': 'Test Amenity'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        amenity_id = data['id']

        # Update amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
            headers=self.headers,
            json={'name': 'Updated Amenity'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Amenity')

    def test_admin_manage_place(self):
        """Test admin managing any place."""
        # Create user's place
        user = User(email='user@test.com', first_name='Test', last_name='User')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

        place_data = {
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'owner_id': user.id
        }

        response = self.client.post('/api/v1/places/', 
            headers=self.headers,
            json=place_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Admin modifies place
        place_id = json.loads(response.data)['id']
        response = self.client.put(f'/api/v1/places/{place_id}', 
            headers=self.headers,
            json={'price': 200.0}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['price'], 200.0)

if __name__ == '__main__':
    unittest.main()