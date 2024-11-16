from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from collections.abc import Mapping

class TestPlaceAPI(BaseTestCase):
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
        
        # Créer un token de test
        self.token = "test_token"  # Dans un vrai test, générer un vrai token

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_place(self):
        response = self.client.post(
            '/api/v1/places',
            headers={'Authorization': f'Bearer {self.token}'},
            json={
                'title': 'New Place',
                'description': 'Test description',
                'price': 100.00,
                'owner_id': self.user.id
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['data']['title'], 'New Place')

    def test_get_places(self):
        response = self.client.get('/api/v1/places')
        self.assertEqual(response.status_code, 200)