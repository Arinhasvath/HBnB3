from tests.base import BaseTestCase
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models.base_model import BaseModel
from app.repositories.base_repository import BaseRepository
from collections.abc import Mapping

class TestBaseRepository(BaseTestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        self.repo = BaseRepository(BaseModel)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_and_get(self):
        # Test basique d'ajout et récupération
        pass  # À implémenter selon votre modèle de base

    def test_get_all(self):
        # Test de récupération de tous les éléments
        pass  # À implémenter selon votre modèle de base

    def test_delete(self):
        # Test de suppression
        pass  # À implémenter selon votre modèle de base