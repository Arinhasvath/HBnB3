"""Complete test suite for HBNB project."""
import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from app.db import db
from app.models import User, Place, Review, Amenity
import json

class TestHBNB(unittest.TestCase):
    """Test suite for HBNB project."""

    @classmethod
    def setUpClass(cls):
        """Setup test environment."""
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        # Create test users
        with cls.app.app_context():
            # Create admin user
            cls.admin = User(
                email='admin@test.com',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            cls.admin.set_password('admin123')
            db.session.add(cls.admin)

            # Create regular user
            cls.user = User(
                email='user@test.com',
                first_name='Test',
                last_name='User',
                is_admin=False
            )
            cls.user.set_password('user123')
            db.session.add(cls.user)
            
            db.session.commit()

            # Create tokens
            cls.admin_token = create_access_token(
                identity={'id': cls.admin.id, 'is_admin': True}
            )
            cls.user_token = create_access_token(
                identity={'id': cls.user.id, 'is_admin': False}
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Setup before each test."""
        db.session.begin_nested()

    def tearDown(self):
        """Cleanup after each test."""
        db.session.rollback()
        db.session.remove()

    # Authentication Tests
    def test_login(self):
        """Test user login."""
        response = self.client.post('/api/v1/auth/login',
            json={
                'email': 'user@test.com',
                'password': 'user123'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_invalid_login(self):
        """Test invalid login."""
        response = self.client.post('/api/v1/auth/login',
            json={
                'email': 'user@test.com',
                'password': 'wrong'
            }
        )
        self.assertEqual(response.status_code, 401)

    # User Tests
    def test_create_user(self):
        """Test user creation."""
        response = self.client.post('/api/v1/users/',
            json={
                'email': 'new@test.com',
                'password': 'newpass123',
                'first_name': 'New',
                'last_name': 'User'
            },
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 201)

    def test_duplicate_email(self):
        """Test duplicate email prevention."""
        response = self.client.post('/api/v1/users/',
            json={
                'email': 'user@test.com',
                'password': 'test123',
                'first_name': 'Test',
                'last_name': 'User'
            },
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 400)

    # Place Tests
    def test_create_place(self):
        """Test place creation."""
        response = self.client.post('/api/v1/places/',
            json={
                'title': 'Test Place',
                'description': 'Test Description',
                'price': 100.0,
                'latitude': 40.7128,
                'longitude': -74.0060
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        return data['id']

    def test_get_places(self):
        """Test getting places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    # Review Tests
    def test_create_review(self):
        """Test review creation."""
        place_id = self.test_create_place()
        response = self.client.post('/api/v1/reviews/',
            json={
                'text': 'Great place!',
                'rating': 5,
                'place_id': place_id
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 201)

    # Admin Tests
    def test_admin_operations(self):
        """Test admin operations."""
        # Create amenity (admin only)
        response = self.client.post('/api/v1/amenities/',
            json={'name': 'WiFi'},
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 201)
        amenity_id = json.loads(response.data)['id']

        # Update amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
            json={'name': 'High-Speed WiFi'},
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Regular user can't modify amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
            json={'name': 'Should Fail'},
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_manage_users(self):
        """Test admin user management."""
        # Create user
        response = self.client.post('/api/v1/users/',
            json={
                'email': 'managed@test.com',
                'password': 'pass123',
                'first_name': 'Managed',
                'last_name': 'User'
            },
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 201)
        user_id = json.loads(response.data)['id']

        # Update user
        response = self.client.put(f'/api/v1/users/{user_id}',
            json={'first_name': 'Updated'},
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_search_places(self):
        """Test place search functionality."""
        # Create test places
        self.client.post('/api/v1/places/',
            json={
                'title': 'Cheap Place',
                'price': 50.0,
                'description': 'Budget friendly'
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.client.post('/api/v1/places/',
            json={
                'title': 'Luxury Place',
                'price': 200.0,
                'description': 'High end'
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )

        # Test price filter
        response = self.client.get('/api/v1/places/search?price_max=100')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(any(p['title'] == 'Cheap Place' for p in data))
        self.assertFalse(any(p['title'] == 'Luxury Place' for p in data))

if __name__ == '__main__':
    unittest.main()
