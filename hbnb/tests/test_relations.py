from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from collections.abc import Mapping

class TestRelations(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_place_relation(self):
        user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()

        place = Place(
            title='Test Place',
            price=100.0,
            owner_id=user.id
        )
        db.session.add(place)
        db.session.commit()

        self.assertEqual(place.owner_id, user.id)
        self.assertIn(place, user.places)