"""User tests."""
from tests.base import TestBase
from app.models import User
from app.db import db

class TestUser(TestBase):
    """Test user model and operations."""

    def test_create_user(self):
        """Test simple user creation."""
        user = User(
            email='test@test.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(email='test@test.com').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'test@test.com')