# tests/test_models/test_review.py
import pytest
from app import create_app, db

def test_create_review():
    app = create_app('testing')
    
    with app.app_context():
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        
        # Créer un utilisateur
        user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        
        # Créer un lieu
        place = Place(
            title='Test Place',
            description='Test Description',
            price=100.0,
            owner_id=user.id
        )
        db.session.add(place)
        db.session.commit()
        
        # Créer une review
        review = Review(
            text='Great place!',
            rating=5,
            user_id=user.id,
            place_id=place.id
        )
        db.session.add(review)
        db.session.commit()
        
        assert review.id is not None
        assert review.rating == 5