"""test_place_repository.py"""
import unittest
from app.repositories.place_repository import PlaceRepository
from app.models.place import Place
from app.models.user import User
from app import db, create_app

class TestPlaceRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
            self.repo = PlaceRepository()
            self.user = User(
                email='test@test.com',
                password='test123',
                first_name='Test',
                last_name='User'
            )
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_place(self):
        with self.app.app_context():
            place = Place(
                title='Test Place',
                description='Test Description',
                price=100.0,
                owner_id=self.user.id
            )
            saved_place = self.repo.add(place)
            self.assertEqual(saved_place.title, 'Test Place')

    def test_get_by_price_range(self):
        with self.app.app_context():
            place1 = Place(title='Place 1', price=50, owner_id=self.user.id)
            place2 = Place(title='Place 2', price=150, owner_id=self.user.id)
            self.repo.add(place1)
            self.repo.add(place2)

            results = self.repo.get_by_price_range(40, 60)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].price, 50)