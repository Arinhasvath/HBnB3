"""Test suite for model relations."""
import unittest
from app import create_app
from app.db import db
from app.models import User, Place, Review, Amenity
from datetime import datetime

class TestRelations(unittest.TestCase):
    """Test cases for model relations."""

    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test data
        self.owner = User(
            email='owner@test.com',
            first_name='Owner',
            last_name='Test',
            is_admin=False
        )
        self.owner.set_password('password')
        
        self.reviewer = User(
            email='reviewer@test.com',
            first_name='Reviewer',
            last_name='Test',
            is_admin=False
        )
        self.reviewer.set_password('password')
        
        db.session.add_all([self.owner, self.reviewer])
        db.session.commit()

    def tearDown(self):
        """Clean up test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_place_user_relationship(self):
        """Test relationship between Place and User."""
        place = Place(
            title="Test Place",
            description="Test Description",
            price=100.0,
            owner_id=self.owner.id
        )
        db.session.add(place)
        db.session.commit()
        
        self.assertEqual(place.owner, self.owner)
        self.assertIn(place, self.owner.places)

    def test_place_amenities_relationship(self):
        """Test relationship between Place and Amenities."""
        amenities = [
            Amenity(name="WiFi"),
            Amenity(name="Pool")
        ]
        db.session.add_all(amenities)
        
        place = Place(
            title="Place with Amenities",
            description="Test Description",
            price=150.0,
            owner_id=self.owner.id,
            amenities=amenities
        )
        db.session.add(place)
        db.session.commit()
        
        self.assertEqual(len(place.amenities), 2)
        for amenity in amenities:
            self.assertIn(place, amenity.places)

    def test_place_reviews_relationship(self):
        """Test relationship between Place and Reviews."""
        place = Place(
            title="Place to Review",
            description="Test Description",
            price=200.0,
            owner_id=self.owner.id
        )
        db.session.add(place)
        
        review = Review(
            text="Great place!",
            rating=5,
            user_id=self.reviewer.id,
            place_id=place.id
        )
        db.session.add(review)
        db.session.commit()
        
        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(review.place, place)
        self.assertEqual(review.user, self.reviewer)
        self.assertIn(review, self.reviewer.reviews)

if __name__ == '__main__':
    unittest.main()