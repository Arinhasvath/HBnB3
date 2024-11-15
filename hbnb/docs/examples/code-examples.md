# 💻 Exemples de Code HBNB

## 📁 Structure des Exemples
```
docs/examples/
├── authentication/
│   ├── login.py
│   └── register.py
├── places/
│   ├── create_place.py
│   └── search_places.py
├── bookings/
│   └── create_booking.py
└── reviews/
    └── add_review.py
```

## 🔐 Exemples d'Authentification
```python
# docs/examples/authentication/login.py
import requests

def login_example():
    url = "https://api.hbnb.com/v1/auth/login"
    data = {
        "email": "user@example.com",
        "password": "password123"
    }
    
    response = requests.post(url, json=data)
    print(response.json())

# docs/examples/authentication/register.py
def register_example():
    url = "https://api.hbnb.com/v1/auth/register"
    data = {
        "email": "newuser@example.com",
        "password": "securePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    response = requests.post(url, json=data)
    print(response.json())
```

Reprenons le code-examples.md et complétons-le :

```markdown
# 💻 Exemples de Code HBNB

## 🏠 Exemples Places

```python
# Création d'un nouveau logement
from app.models import Place
from app.db import db

def create_place_example():
    new_place = Place(
        title="Villa Vue Mer",
        description="Magnifique villa avec vue sur l'océan",
        price=200.00,
        owner_id="user_uuid",
        latitude=43.5,
        longitude=-1.5
    )
    
    try:
        db.session.add(new_place)
        db.session.commit()
        return new_place.to_dict()
    except Exception as e:
        db.session.rollback()
        raise e

# Recherche de logements
def search_places_example():
    places = Place.query.filter(
        Place.price.between(100, 300),
        Place.latitude.between(43.0, 44.0)
    ).all()
    return [place.to_dict() for place in places]
```

## ⭐ Exemples Reviews

```python
# Ajout d'un avis
from app.models import Review

def add_review_example():
    review = Review(
        text="Séjour parfait! Vue magnifique et hôte accueillant.",
        rating=5,
        place_id="place_uuid",
        user_id="user_uuid"
    )
    
    try:
        db.session.add(review)
        db.session.commit()
        return review.to_dict()
    except Exception as e:
        db.session.rollback()
        raise e

# Récupération des avis d'un logement
def get_place_reviews(place_id):
    reviews = Review.query.filter_by(place_id=place_id)\
                         .order_by(Review.created_at.desc())\
                         .all()
    return [review.to_dict() for review in reviews]
```

## 🏨 Exemples Amenities

```python
# Ajout d'équipements à un logement
from app.models import Amenity

def add_amenities_example():
    # Création des équipements
    wifi = Amenity(name="WiFi")
    pool = Amenity(name="Piscine")
    
    # Ajout à un logement
    place = Place.query.get("place_uuid")
    place.amenities.extend([wifi, pool])
    
    try:
        db.session.commit()
        return place.to_dict()
    except Exception as e:
        db.session.rollback()
        raise e
```

## 📅 Exemples Réservations

```python
# Création d'une réservation
from app.models import Booking
from datetime import datetime, timedelta

def create_booking_example():
    check_in = datetime.now() + timedelta(days=7)
    check_out = check_in + timedelta(days=3)
    
    booking = Booking(
        place_id="place_uuid",
        user_id="user_uuid",
        check_in=check_in,
        check_out=check_out,
        guests=2,
        total_price=600.00
    )
    
    try:
        db.session.add(booking)
        db.session.commit()
        return booking.to_dict()
    except Exception as e:
        db.session.rollback()
        raise e
```

## 🔍 Exemples de Recherche Avancée

```python
# Recherche avec filtres multiples
def advanced_search_example():
    from sqlalchemy import and_
    
    filters = [
        Place.price.between(100, 300),
        Place.latitude.between(43.0, 44.0)
    ]
    
    # Ajout de filtres optionnels
    if amenities:
        filters.append(Place.amenities.any(Amenity.name.in_(amenities)))
    
    places = Place.query.filter(and_(*filters))\
                       .order_by(Place.created_at.desc())\
                       .paginate(page=1, per_page=20)
    
    return {
        'items': [place.to_dict() for place in places.items],
        'total': places.total,
        'pages': places.pages
    }
```

## 🔐 Exemples de Sécurité

```python
# Validation de token
from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token manquant'}), 401
            
        try:
            # Vérification du token
            data = verify_token(token)
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token invalide'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# Utilisation du décorateur
@app.route('/api/v1/profile')
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict())
```

## 📊 Exemples de Stats

```python
# Statistiques de réservation
def get_booking_stats():
    from sqlalchemy import func
    
    stats = db.session.query(
        func.count(Booking.id).label('total_bookings'),
        func.avg(Booking.total_price).label('average_price'),
        func.sum(Booking.total_price).label('total_revenue')
    ).first()
    
    return {
        'total_bookings': stats.total_bookings,
        'average_price': float(stats.average_price),
        'total_revenue': float(stats.total_revenue)
    }
```
