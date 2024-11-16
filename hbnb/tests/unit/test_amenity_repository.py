from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.amenity import Amenity
from collections.abc import Mapping

class TestAmenityRepository(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_amenity(self):
        amenity = Amenity(name='WiFi')
        db.session.add(amenity)
        db.session.commit()
        self.assertIsNotNone(amenity.id)