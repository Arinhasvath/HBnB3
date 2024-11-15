# 🧪 Guide des Tests HBNB

## 📋 Table des Matières
1. [Tests Unitaires](#tests-unitaires)
2. [Tests d'Intégration](#tests-dintégration)
3. [Tests API](#tests-api)
4. [Tests de Performance](#tests-de-performance)
5. [Tests de Sécurité](#tests-de-sécurité)

## 🔬 Tests Unitaires

### Configuration
```python
# tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
```

### Tests des Modèles
```python
# tests/unit/test_models.py
def test_user_creation(db_session):
    user = User(
        email='test@test.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('password123')
    
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.check_password('password123')

def test_place_validation(db_session):
    place = Place(
        title='Test Place',
        price=-10  # Prix invalide
    )
    
    with pytest.raises(ValueError):
        place.validate()
```

## 🔄 Tests d'Intégration

### Tests des Relations
```python
def test_user_place_relationship(db_session):
    user = User(
        email='owner@test.com',
        first_name='Owner',
        last_name='Test'
    )
    db_session.add(user)
    
    place = Place(
        title='Test Place',
        price=100,
        owner_id=user.id
    )
    db_session.add(place)
    db_session.commit()
    
    assert place in user.places
    assert place.owner == user

def test_place_reviews(db_session):
    # Créer utilisateur et place
    user = User(email='user@test.com', first_name='Test', last_name='User')
    place = Place(title='Test Place', price=100, owner_id=user.id)
    
    # Ajouter review
    review = Review(
        text='Great place!',
        rating=5,
        user_id=user.id,
        place_id=place.id
    )
    
    db_session.add_all([user, place, review])
    db_session.commit()
    
    assert review in place.reviews
    assert review.user == user
```

## 🌐 Tests API

### Tests des Endpoints
```python
def test_create_place(client, auth_token):
    response = client.post(
        '/api/v1/places',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'title': 'New Place',
            'description': 'Test description',
            'price': 100.00
        }
    )
    
    assert response.status_code == 201
    assert response.json['data']['title'] == 'New Place'

def test_search_places(client):
    response = client.get('/api/v1/places/search?location=Paris')
    
    assert response.status_code == 200
    assert 'items' in response.json['data']
```

## 📊 Tests de Performance

### Configuration Locust
```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between

class HBNBUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@test.com",
            "password": "password123"
        })
        self.token = response.json()['data']['access_token']
    
    @task(3)
    def view_places(self):
        self.client.get("/api/v1/places")
    
    @task(2)
    def search_places(self):
        self.client.get(
            "/api/v1/places/search",
            params={"location": "Paris"}
        )
```

### Tests de Charge
```bash
# Lancer les tests de charge
locust -f tests/performance/locustfile.py --host=http://localhost:5000
```

## 🔒 Tests de Sécurité

### Tests d'Authentification
```python
def test_invalid_token(client):
    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': 'Bearer invalid_token'}
    )
    assert response.status_code == 401

def test_password_security(db_session):
    user = User(email='test@test.com')
    
    # Test mot de passe faible
    with pytest.raises(ValueError):
        user.set_password('123')
        
    # Test hachage correct
    user.set_password('StrongPass123!')
    assert user.password != 'StrongPass123!'
```

### Tests de Validation
```python
def test_xss_prevention(client):
    response = client.post(
        '/api/v1/places',
        json={
            'title': '<script>alert("xss")</script>'
        }
    )
    assert response.status_code == 400

def test_sql_injection(client):
    response = client.get('/api/v1/users?id=1 OR 1=1')
    assert response.status_code == 400
```

## 🔄 Tests de Bout en Bout (E2E)

### Configuration Selenium
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_booking_flow(driver):
    # Login
    driver.get("http://localhost:5000/login")
    driver.find_element(By.ID, "email").send_keys("test@test.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "submit").click()
    
    # Recherche
    driver.find_element(By.ID, "search").send_keys("Paris")
    driver.find_element(By.ID, "search-button").click()
    
    # Sélection et réservation
    driver.find_element(By.CLASS_NAME, "place-card").click()
    driver.find_element(By.ID, "book-button").click()
    
    # Vérification
    success_message = driver.find_element(By.CLASS_NAME, "success-message")
    assert "Réservation confirmée" in success_message.text
```

## 📈 Couverture des Tests

### Configuration Coverage
```ini
# .coveragerc
[run]
source = app
omit = 
    app/tests/*
    app/migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

### Exécution avec Couverture
```bash
# Lancer les tests avec couverture
pytest --cov=app tests/

# Générer rapport HTML
pytest --cov=app --cov-report=html tests/
```

## 🔄 Intégration Continue

### Configuration GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Run tests
      run: |
        pytest --cov=app tests/
        
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```
