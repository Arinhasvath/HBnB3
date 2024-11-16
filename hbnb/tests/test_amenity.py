import pytest
from app import create_app, db
from app.models.amenity import Amenity

@pytest.fixture(scope='module')
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_amenity(test_app):
    with test_app.app_context():
        amenity = Amenity(name='WiFi')
        db.session.add(amenity)
        db.session.commit()
        
        assert amenity.id is not None
        assert amenity.name == 'WiFi'