from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.place import Place
from app.models.user import User
from app.repositories.place_repository import PlaceRepository
from collections.abc import Mapping

class TestPlaceRepository(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        self.user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(self.user)
        db.session.commit()
        
        self.repo = PlaceRepository()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_place(self):
        place = Place(
            title='Test Place',
            description='Test description',
            price=100.0,
            owner_id=self.user.id
        )
        added_place = self.repo.add(place)
        self.assertIsNotNone(added_place.id)
        self.assertEqual(added_place.title, 'Test Place')

    def test_get_by_location(self):
        place = Place(
            title='Test Place',
            price=100.0,
            owner_id=self.user.id,
            latitude=48.8566,
            longitude=2.3522
        )
        self.repo.add(place)
        
        places = self.repo.get_by_location(48.8566, 2.3522, radius=10)
        self.assertTrue(len(places) > 0)