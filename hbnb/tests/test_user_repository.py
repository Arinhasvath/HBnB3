#!/usr/bin/env python3
"""Tests for user repository."""
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.db import db

class TestUserRepository(unittest.TestCase):
    """Test cases for UserRepository"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            'email': 'test@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_admin': False
        }
        user = self.repo.create_user(user_data)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertFalse(user.is_admin)

    def test_get_user_by_email(self):
        """Test getting user by email"""
        # Create test user
        user_data = {
            'email': 'test@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        created_user = self.repo.create_user(user_data)
        
        # Test retrieving user
        retrieved_user = self.repo.get_by_email('test@test.com')
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, created_user.id)
        self.assertEqual(retrieved_user.email, 'test@test.com')

    def test_is_admin(self):
        """Test admin status check"""
        # Create admin user
        admin_data = {
            'email': 'admin@test.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_admin': True
        }
        admin = self.repo.create_user(admin_data)
        
        # Create regular user
        user_data = {
            'email': 'user@test.com',
            'password': 'user123',
            'first_name': 'Regular',
            'last_name': 'User',
            'is_admin': False
        }
        user = self.repo.create_user(user_data)
        
        # Test admin status
        self.assertTrue(self.repo.is_admin(admin.id))
        self.assertFalse(self.repo.is_admin(user.id))

    def test_authenticate_user(self):
        """Test user authentication"""
        # Create test user
        user_data = {
            'email': 'test@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.repo.create_user(user_data)
        
        # Test successful authentication
        authenticated_user = self.repo.authenticate('test@test.com', 'password123')
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.email, 'test@test.com')
        
        # Test failed authentication
        failed_auth = self.repo.authenticate('test@test.com', 'wrongpassword')
        self.assertIsNone(failed_auth)

    def test_update_user(self):
        """Test updating user"""
        # Create test user
        user_data = {
            'email': 'test@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        user = self.repo.create_user(user_data)
        
        # Update user
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        updated_user = self.repo.update_user(user.id, update_data)
        
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')
        self.assertEqual(updated_user.email, 'test@test.com')  # Email should not change

    def test_delete_user(self):
        """Test deleting user"""
        # Create test user
        user_data = {
            'email': 'test@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        user = self.repo.create_user(user_data)
        
        # Delete user
        result = self.repo.delete_user(user.id)
        self.assertTrue(result)
        
        # Verify user is deleted
        deleted_user = self.repo.get(user.id)
        self.assertIsNone(deleted_user)

if __name__ == '__main__':
    unittest.main()