from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from collections.abc import Mapping

class TestReviewAPI(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        # Créer utilisateur et place pour les tests
        self.user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        self.place = Place(
            title='Test Place',
            price=100.0,
            owner_id=self.user.id
        )
        db.session.add_all([self.user, self.place])
        db.session.commit()
        
        # Token de test
        self.token = "test_token"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_review(self):
        response = self.client.post(
            f'/api/v1/places/{self.place.id}/reviews',
            headers={'Authorization': f'Bearer {self.token}'},
            json={
                'rating': 5,
                'text': 'Great place!'
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['data']['rating'], 5)

    def test_get_place_reviews(self):
        # Créer une review d'abord
        review = Review(
            text='Test review',
            rating=4,
            user_id=self.user.id,
            place_id=self.place.id
        )
        db.session.add(review)
        db.session.commit()

        response = self.client.get(f'/api/v1/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json['data']) > 0)