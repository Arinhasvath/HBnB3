"""Test suite for HBnB."""
from tests.base import TestBase
from app.models import User
from werkzeug.security import generate_password_hash
import json

class TestHBnB(TestBase):
    """Test cases for HBnB."""

    def test_create_user(self):
        """Test user creation."""
        user_data = {
            'email': 'test@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'test123'
        }
        response = self.client.post(
            '/api/v1/users/',
            json=user_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], user_data['email'])

if __name__ == '__main__':
    unittest.main()