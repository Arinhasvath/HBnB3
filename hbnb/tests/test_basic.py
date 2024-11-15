"""Basic test to verify setup."""
import unittest
from app import create_app
from app.db import db

class TestBasic(unittest.TestCase):
    """Basic test case."""

    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up test environment."""
        with self.app.app_context():
            db.session.remove()
        self.app_context.pop()

    def test_app_exists(self):
        """Test if app exists."""
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        """Test if app is in testing mode."""
        self.assertTrue(self.app.config['TESTING'])

if __name__ == '__main__':
    unittest.main()