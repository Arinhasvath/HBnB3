from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from sqlalchemy.exc import IntegrityError
from collections.abc import Mapping

class TestErrorHandling(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_duplicate_email(self):
        # Test pour email dupliqué
        user1 = User(
            email='test@test.com',
            password='test123',
            first_name='Test1',
            last_name='User1'
        )
        db.session.add(user1)
        db.session.commit()

        user2 = User(
            email='test@test.com',  # Même email
            password='test456',
            first_name='Test2',
            last_name='User2'
        )
        db.session.add(user2)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_invalid_price(self):
        user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()

        with self.assertRaises(ValueError):
            place = Place(
                title='Test Place',
                price=-100.0,  # Prix négatif
                owner_id=user.id
            )
            place.validate()