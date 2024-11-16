from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from collections.abc import Mapping

class TestPlaceAmenitiesAPI(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        # Créer un utilisateur
        self.user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(self.user)
        db.session.commit()

        # Créer un lieu
        self.place = Place(
            title='Test Place',
            price=100.0,
            owner_id=self.user.id
        )
        db.session.add(self.place)

        # Créer des amenities
        self.amenity = Amenity(name='WiFi')
        db.session.add(self.amenity)
        db.session.commit()

        self.token = "test_token"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_amenity_to_place(self):
        response = self.client.post(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Vérifier que l'amenity a été ajoutée
        place = Place.query.get(self.place.id)
        self.assertIn(self.amenity, place.amenities)

    def test_get_place_amenities(self):
        # Ajouter une amenity au lieu
        self.place.amenities.append(self.amenity)
        db.session.commit()

        response = self.client.get(f'/api/v1/places/{self.place.id}/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['data']), 1)