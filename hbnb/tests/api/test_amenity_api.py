from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.amenity import Amenity
from collections.abc import Mapping

class TestAmenityAPI(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        self.token = "test_token"  # Pour l'authentification

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_amenity(self):
        response = self.client.post(
            '/api/v1/amenities',
            headers={'Authorization': f'Bearer {self.token}'},
            json={'name': 'WiFi'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['data']['name'], 'WiFi')

    def test_get_amenities(self):
        # Créer quelques amenities de test
        amenities = [
            Amenity(name='WiFi'),
            Amenity(name='Pool'),
            Amenity(name='Parking')
        ]
        for amenity in amenities:
            db.session.add(amenity)
        db.session.commit()

        response = self.client.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['data']), 3)