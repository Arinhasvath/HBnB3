# tests/test_models/test_place.py
import pytest
from app import create_app, db

def test_create_place():
    app = create_app('testing')
    
    with app.app_context():
        from app.models.user import User
        from app.models.place import Place
        
        # Créer un propriétaire
        owner = User(
            email='owner@test.com',
            password='test123',
            first_name='Owner',
            last_name='User'
        )
        db.session.add(owner)
        db.session.commit()
        
        # Créer un lieu
        place = Place(
            title='Beach House',
            description='Beautiful beachfront property',
            price=150.0,
            owner_id=owner.id
        )
        db.session.add(place)
        db.session.commit()
        
        assert place.id is not None
        assert place.title == 'Beach House'
        assert place.owner_id == owner.id