```markdown
# 📚 Documentation API de Référence HBNB

## 🌐 Informations Générales

- Base URL: `https://api.hbnb.com/v1`
- Format: JSON
- Authentification: Bearer Token

## 🔐 Endpoints Authentification

### Création de compte
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securePass123",
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
        "created_at": "2024-11-14T12:00:00Z"
    }
}
```

### Connexion
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securePass123"
}

# Réponse (200 OK)
{
    "status": "success",
    "data": {
        "access_token": "eyJhbGciOiJ...",
        "refresh_token": "eyJhbGciOi...",
        "expires_in": 3600
    }
}
```

### Rafraîchir Token
```http
POST /auth/refresh
Authorization: Bearer {refresh_token}

# Réponse (200 OK)
{
    "status": "success",
    "data": {
        "access_token": "eyJhbGciOiJ...",
        "expires_in": 3600
    }
}
```

## 👤 Endpoints Utilisateurs

### Profil Utilisateur
```http
GET /users/me
Authorization: Bearer {token}

# Réponse (200 OK)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "places": [...],
        "reviews": [...]
    }
}
```

### Mettre à jour Profil
```http
PUT /users/me
Authorization: Bearer {token}
Content-Type: application/json

{
    "first_name": "John Updated",
    "last_name": "Doe Updated"
}

# Réponse (200 OK)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John Updated",
        "last_name": "Doe Updated"
    }
}
```

## 🏠 Endpoints Places

### Créer un Logement
```http
POST /places
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Villa Vue Mer",
    "description": "Magnifique villa...",
    "price": 200.00,
    "latitude": 43.5,
    "longitude": -1.5,
    "amenities": ["wifi", "pool"]
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "title": "Villa Vue Mer",
        "price": 200.00,
        "created_at": "2024-11-14T12:00:00Z"
    }
}
```

### Recherche de Logements
```http
GET /places/search
Query Parameters:
- location (string, optional)
- min_price (float, optional)
- max_price (float, optional)
- amenities (array, optional)
- check_in (date, optional)
- check_out (date, optional)

# Réponse (200 OK)
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

## ⭐ Endpoints Reviews

### Créer un Avis
```http
POST /places/{place_id}/reviews
Authorization: Bearer {token}
Content-Type: application/json

{
    "rating": 5,
    "text": "Séjour parfait!"
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "rating": 5,
        "text": "Séjour parfait!",
        "created_at": "2024-11-14T12:00:00Z"
    }
}
```

### Liste des Avis d'un Logement
```http
GET /places/{place_id}/reviews

# Réponse (200 OK)
{
    "status": "success",
    "data": {
        "items": [...],
        "total": 10,
        "page": 1,
        "per_page": 20
    }
}
```

## 🛎️ Endpoints Amenities

### Liste des Équipements
```http
GET /amenities

# Réponse (200 OK)
{
    "status": "success",
    "data": [
        {
            "id": "uuid",
            "name": "WiFi"
        },
        {
            "id": "uuid",
            "name": "Piscine"
        }
    ]
}
```

## 📅 Endpoints Réservations

### Créer une Réservation
```http
POST /places/{place_id}/bookings
Authorization: Bearer {token}
Content-Type: application/json

{
    "check_in": "2024-12-01",
    "check_out": "2024-12-05",
    "guests": 2
}

# Réponse (201 Created)
{
    "status": "success",
    "data": {
        "id": "uuid",
        "check_in": "2024-12-01",
        "check_out": "2024-12-05",
        "total_price": 800.00,
        "status": "pending"
    }
}
```

## ⚠️ Gestion des Erreurs

### Format des Erreurs
```json
{
    "status": "error",
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "field": ["error message"]
        }
    }
}
```

### Codes d'Erreur Communs
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity
- 429: Too Many Requests
- 500: Internal Server Error

## 📊 Pagination

Tous les endpoints qui retournent des listes supportent la pagination:

```http
GET /endpoint?page=1&per_page=20

# Réponse
{
    "status": "success",
    "data": {
        "items": [...],
        "total": 100,
        "page": 1,
        "per_page": 20,
        "pages": 5
    }
}
```
