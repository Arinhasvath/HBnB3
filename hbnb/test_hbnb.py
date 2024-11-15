import unittest
from app import create_app, db
from app.models import User, Place, Review, Amenity
from werkzeug.security import generate_password_hash

class TestHBnB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configure the test client and create a test database."""
        cls.app = create_app('testing')  # Assurez-vous d'avoir une configuration de test
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()  # Créez toutes les tables

    @classmethod
    def tearDownClass(cls):
        """Clean up the database after tests."""
        with cls.app.app_context():
            db.drop_all()  # Supprimez toutes les tables

    def setUp(self):
        """Create a new user and other entities for testing."""
        self.admin_email = 'admin@hbnb.io'
        self.admin_password = 'admin1234'
        self.admin = User(
            id='36c9050e-ddd3-4c3b-9731-9f487208bbc1',
            email=self.admin_email,
            first_name='Admin',
            last_name='HBnB',
            password=generate_password_hash(self.admin_password),
            is_admin=True
        )
        with self.app.app_context():
            db.session.add(self.admin)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def test_create_user(self):
        """Test user creation."""
        user = User(email='user@example.com', password='password', first_name='John', last_name='Doe')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='user@example.com').first())

    def test_create_place(self):
        """Test place creation."""
        place = Place(
            id='1',
            title='Luxurious Villa',
            description='A beautiful villa with stunning views.',
            price=250.00,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id=self.admin.id
        )
        with self.app.app_context():
            db.session.add(place)
            db.session.commit()
            self.assertIsNotNone(Place.query.filter_by(title='Luxurious Villa').first())

    def test_create_review(self):
        """Test review creation."""
        place = Place(
            id='1',
            title='Luxurious Villa',
            description='A beautiful villa with stunning views.',
            price=250.00,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id=self.admin.id
        )
        review = Review(
            id='1',
            text='Amazing stay!',
            rating=5,
            user_id=self.admin.id,
            place_id=place.id
        )
        with self.app.app_context():
            db.session.add(place)
            db.session.add(review)
            db.session.commit()
            self.assertIsNotNone(Review.query.filter_by(text='Amazing stay!').first())

    def test_create_amenity(self):
        """Test amenity creation."""
        amenity = Amenity(id='1', name='WiFi')
        with self.app.app_context():
            db.session.add(amenity)
            db.session.commit()
            self.assertIsNotNone(Amenity.query.filter_by(name='WiFi').first())

    def test_place_amenity_relationship(self):
        """Test many-to-many relationship between places and amenities."""
        place = Place(
            id='1',
            title='Luxurious Villa',
            description='A beautiful villa with stunning views.',
            price=250.00,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id=self.admin.id
        )
        amenity = Amenity(id='1', name='WiFi')

        with self.app.app_context():
            db.session.add(place)
            db.session.add(amenity)
            db.session.commit()

            place.amenities.append(amenity)
            db.session.commit()

            self.assertIn(amenity, place.amenities)

    def test_user_review_relationship(self):
        """Test one-to-many relationship between user and reviews."""
        place = Place(
            id='1',
            title='Luxurious Villa',
            description='A beautiful villa with stunning views.',
            price=250.00,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id=self.admin.id
        )
        review = Review(
            id='1',
            text='Amazing stay!',
            rating=5,
            user_id=self.admin.id,
            place_id=place.id
        )
        with self.app.app_context():
            db.session.add(place)
            db.session.add(review)
            db.session.commit()

            self.assertIn(review, self.admin.reviews)

if __name__ == '__main__':
    unittest.main()