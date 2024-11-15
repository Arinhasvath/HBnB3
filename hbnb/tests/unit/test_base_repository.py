"""test_base_repository.py"""
import unittest
from app import create_app, db
from app.models.user import User

class TestBaseRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_and_get(self):
        user = User(email='test@test.com', 
                   password='test123',
                   first_name='Test',
                   last_name='User')
        db.session.add(user)
        db.session.commit()
        
        fetched_user = User.query.first()
        self.assertEqual(fetched_user.email, 'test@test.com')