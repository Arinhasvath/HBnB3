# 🚀 Documentation API HBNB v1.0.0

## 📋 Table des Matières
1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Users API](#users-api)
4. [Places API](#places-api)
5. [Reviews API](#reviews-api)
6. [Bookings API](#bookings-api)
7. [Amenities API](#amenities-api)
8. [Rate Limits](#rate-limits)
9. [Erreurs](#erreurs)

## 🌟 Introduction

Base URL: `https://api.hbnb.com/v1`

### Format Standard des Réponses
```json
{
    "status": "success|error",
    "data": {},
    "message": "Description",
    "timestamp": "2024-11-14T12:00:00Z"
}
```

## 🔐 Authentication

### Obtenir un Token
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

# Réponse
{
    "status": "success",
    "data": {
        "access_token": "eyJhbGciOiJ...",
        "refresh_token": "eyJhbGciOi...",
        "expires_in": 3600
    }
}
```

### Headers Requis
```http
Authorization: Bearer eyJhbGciOiJ...
```

## 👥 Users API

### Créer un Utilisateur
```http
POST /users
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securePass123!",
    "first_name": "John",
    "last_name": "Doe"
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "created_at": "2024-11-14T12:00:00Z"
    }
}
```

### Profil Utilisateur
```http
GET /users/me
Authorization: Bearer {token}

# Réponse
{
    "status": "success",
    "data": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "created_at": "2024-11-14T12:00:00Z",
        "places": [...],
        "reviews": [...]
    }
}
```

## 🏠 Places API

### Créer un Logement
```http
POST /places
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Beautiful Beach House",
    "description": "Luxurious beachfront property...",
    "price": 150.00,
    "latitude": 43.12345,
    "longitude": -79.98765,
    "amenities": ["wifi", "pool"]
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "title": "Beautiful Beach House",
        "price": 150.00,
        "created_at": "2024-11-14T12:00:00Z",
        "owner": {
            "id": "uuid",
            "name": "John Doe"
        }
    }
}
```

### Recherche de Logements
```http
GET /places/search
Query Parameters:
- location (string): Ville ou coordonnées
- min_price (float): Prix minimum
- max_price (float): Prix maximum
- amenities (array): ["wifi", "pool"]
- check_in (date): Date d'arrivée
- check_out (date): Date de départ
- guests (integer): Nombre de voyageurs

# Exemple
GET /places/search?location=Paris&min_price=100&max_price=300

# Réponse
{
    "status": "success",
    "data": {
        "items": [...],
        "total": 45,
        "page": 1,
        "per_page": 20
    }
}
```

## ⭐ Reviews API

### Créer un Avis
```http
POST /places/{place_id}/reviews
Authorization: Bearer {token}
Content-Type: application/json

{
    "rating": 5,
    "text": "Amazing place, great host!"
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "rating": 5,
        "text": "Amazing place, great host!",
        "created_at": "2024-11-14T12:00:00Z",
        "user": {
            "id": "uuid",
            "name": "John Doe"
        }
    }
}
```

## 📅 Bookings API

### Créer une Réservation
```http
POST /places/{place_id}/bookings
Authorization: Bearer {token}
Content-Type: application/json

{
    "check_in": "2024-12-01",
    "check_out": "2024-12-05",
    "guests": 2,
    "message": "Looking forward to staying!"
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "check_in": "2024-12-01",
        "check_out": "2024-12-05",
        "total_price": 750.00,
        "status": "pending"
    }
}
```

## 🛎️ Amenities API

### Liste des Équipements
```http
GET /amenities

# Réponse
{
    "status": "success",
    "data": [
        {
            "id": "uuid",
            "name": "WiFi",
            "icon": "wifi"
        },
        {
            "id": "uuid",
            "name": "Pool",
            "icon": "pool"
        }
    ]
}
```

## ⚠️ Rate Limits

| Endpoint | Limite |
|----------|--------|
| /auth/* | 5 requêtes/minute |
| /places/search | 30 requêtes/minute |
| /bookings/* | 10 requêtes/minute |
| Autres endpoints | 60 requêtes/minute |

## ❌ Erreurs

### Codes d'Erreur Standard
```json
{
    "status": "error",
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "email": ["Email format is invalid"]
        }
    }
}
```

### Codes HTTP
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity
- 429: Too Many Requests
- 500: Internal Server Error

### Codes d'Erreur Personnalisés
| Code | Description |
|------|-------------|
| VALIDATION_ERROR | Données invalides |
| AUTH_ERROR | Erreur d'authentification |
| BOOKING_CONFLICT | Dates non disponibles |
| PAYMENT_ERROR | Erreur de paiement |
| RESOURCE_NOT_FOUND | Ressource introuvable |

## 📊 Versions et Changements

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2024-11-14 | Version initiale |
| 1.1.0 | 2024-12-01 | Ajout recherche avancée |

## 🔗 Ressources Utiles
- [Guide de Démarrage Rapide](getting-started.md)
- [Guide de Débogage](debugging.md)
- [Exemples de Code](code-examples.md)
```
