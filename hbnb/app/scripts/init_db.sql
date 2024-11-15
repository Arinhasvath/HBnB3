"""Initialize database with required data."""
from app import create_app, db
from app.models import User, Amenity
from werkzeug.security import generate_password_hash
import uuid

def init_db():
    """Initialize database with required data."""
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()

        # Create admin if not exists
        admin = User.query.filter_by(email='admin@hbnb.io').first()
        if not admin:
            admin = User(
                id=str(uuid.uuid4()),
                email='admin@hbnb.io',
                first_name='Admin',
                last_name='HBnB',
                password=generate_password_hash('admin1234'),
                is_admin=True
            )
            db.session.add(admin)

        # Create initial amenities
        initial_amenities = ['WiFi', 'Air Conditioning', 'Swimming Pool']
        for name in initial_amenities:
            if not Amenity.query.filter_by(name=name).first():
                amenity = Amenity(
                    id=str(uuid.uuid4()),
                    name=name
                )
                db.session.add(amenity)

        try:
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    init_db()