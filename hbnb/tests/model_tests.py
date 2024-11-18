"""Test suite for models."""

import unittest
from app import create_app
from app.db import db
from app.models import User, Place, Review, Amenity
from werkzeug.security import check_password_hash
from collections.abc import Mapping


class TestModels(unittest.TestCase):
    """Test cases for all models."""

    def setUp(self):
        """Set up test environment."""
        self.app = create_app("testing")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create test admin user
        self.admin = User(
            email="admin@test.com",
            first_name="Admin",
            last_name="Test",
            is_admin=True,
        )
        self.admin.set_password("admin123")
        db.session.add(self.admin)
        db.session.commit()

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_user_creation(self):
        """Test user creation and validation."""
        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            is_admin=False,
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        # Test retrieval
        retrieved = User.query.filter_by(email="test@example.com").first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.email, "test@example.com")
        self.assertTrue(check_password_hash(retrieved.password, "password123"))

    def test_place_creation(self):
        """Test place creation with relationships."""
        # Create user first
        user = User(
            email="owner@test.com", first_name="Owner", last_name="Test"
        )
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        # Create place
        place = Place(
            title="Test Place",
            description="A test place",
            price=100.0,
            latitude=48.8566,
            longitude=2.3522,
            owner_id=user.id,
        )
        db.session.add(place)
        db.session.commit()

        # Test relationships
        self.assertEqual(place.owner, user)
        self.assertIn(place, user.places)

    def test_review_creation(self):
        """Test review creation with validations."""
        # Create necessary related objects
        user = User(
            email="reviewer@test.com", first_name="Reviewer", last_name="Test"
        )
        user.set_password("pass123")
        db.session.add(user)

        place = Place(
            title="Place to Review",
            description="Test place",
            price=150.0,
            owner_id=self.admin.id,
        )
        db.session.add(place)
        db.session.commit()

        # Create review
        review = Review(
            text="Great place!", rating=5, user_id=user.id, place_id=place.id
        )
        db.session.add(review)
        db.session.commit()

        # Test relationships and constraints
        self.assertEqual(review.user, user)
        self.assertEqual(review.place, place)
        self.assertIn(review, place.reviews)
        self.assertIn(review, user.reviews)

    def test_amenity_creation(self):
        """Test amenity creation and place relationship."""
        # Create amenities
        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Pool")
        db.session.add_all([wifi, pool])

        # Create place with amenities
        place = Place(
            title="Luxury Place",
            description="Place with amenities",
            price=200.0,
            owner_id=self.admin.id,
        )
        place.amenities.extend([wifi, pool])
        db.session.add(place)
        db.session.commit()

        # Test relationships
        self.assertEqual(len(place.amenities), 2)
        self.assertIn(wifi, place.amenities)
        self.assertIn(pool, place.amenities)
        self.assertIn(place, wifi.places)
        self.assertIn(place, pool.places)


if __name__ == "__main__":
    unittest.main()
