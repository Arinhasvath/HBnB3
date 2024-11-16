# tests/test_models/test_user.py
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    _app = create_app('testing')
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return _app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_create_user(init_db):
    """Test creating a user"""
    user = User(
        email='test@test.com',
        password='test123',
        first_name='Test',
        last_name='User'
    )
    db.session.add(user)
    db.session.commit()
    assert user.id is not None
    assert user.email == 'test@test.com'
# tests/test_models/test_user.py - ajoutons ce test
def test_user_password():
    app = create_app('testing')
    
    with app.app_context():
        from app.models.user import User
        
        user = User(
            email='test@test.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Vérifie le hash du mot de passe
        assert user.check_password('test123')
        assert not user.check_password('wrongpass')

def test_find_user():
    app = create_app('testing')
    
    with app.app_context():
        from app.models.user import User
        
        # Créer un utilisateur
        user = User(
            email='find@test.com',
            password='test123',
            first_name='Find',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()
        
        # Rechercher l'utilisateur
        found_user = User.query.filter_by(email='find@test.com').first()
        assert found_user is not None
        assert found_user.email == 'find@test.com'