from tests.base import BaseTestCase
"""test_user_repository.py"""
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.user import User
from tests.unit.test_base_repository import TestBaseRepository
from app.repositories.user_repository import UserRepository
from collections.abc import Mapping

class TestUserRepository(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.repo = UserRepository()

    def test_get_by_email(self):
        user = User(email='test@test.com',
                   password='test123',
                   first_name='Test',
                   last_name='User')
        self.repo.add(user)
        
        found_user = self.repo.get_by_email('test@test.com')
        self.assertEqual(found_user.email, user.email)

    def test_get_by_admin(self):
        admin = User(email='admin@test.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User',
                    is_admin=True)
        self.repo.add(admin)
        
        admins = self.repo.get_by_admin()
        self.assertEqual(len(admins), 1)
        self.assertTrue(admins[0].is_admin)

class TestUserRepository(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, 'test@test.com')