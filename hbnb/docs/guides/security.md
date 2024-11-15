# 🔐 Guide de Sécurité HBNB

## 📋 Table des Matières
1. [Authentification](#authentification)
2. [Autorisation](#autorisation)
3. [Protection des Données](#protection-des-données)
4. [Sécurité des API](#sécurité-des-api)
5. [Bonnes Pratiques](#bonnes-pratiques)

## 🔑 Authentification

### Configuration JWT
```python
JWT_CONFIG = {
    'SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
    'REFRESH_TOKEN_EXPIRES': timedelta(days=30)
}
```

### Hachage des Mots de Passe
```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
```

## 🛡️ Autorisation

### Middleware de Vérification
```python
def auth_required(roles=['user']):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token or not token.startswith('Bearer '):
                return jsonify({'error': 'Token manquant'}), 401
            
            try:
                payload = verify_jwt_token(token.split(' ')[1])
                if payload['role'] not in roles:
                    return jsonify({'error': 'Accès non autorisé'}), 403
            except:
                return jsonify({'error': 'Token invalide'}), 401
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## 🔒 Protection des Données

### Chiffrement des Données Sensibles
```python
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self):
        self.key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()
```

### Masquage des Données Sensibles
```python
class User(BaseModel):
    def to_dict(self):
        data = super().to_dict()
        # Supprimer les données sensibles
        data.pop('password', None)
        data['email'] = self.mask_email(data['email'])
        return data

    @staticmethod
    def mask_email(email):
        username, domain = email.split('@')
        return f"{username[0]}{'*' * (len(username)-2)}{username[-1]}@{domain}"
```

## 🔐 Sécurité des API

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/login")
@limiter.limit("5 per minute")
def login():
    pass
```

### Protection CSRF
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Dans les formulaires
<form method="post">
    {{ form.csrf_token }}
</form>
```

### Headers de Sécurité
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

## ✅ Bonnes Pratiques

### Validation des Entrées
```python
from marshmallow import Schema, fields, validate

class UserInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=[
        validate.Length(min=8),
        validate.Regexp(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)",
            error="Password must contain uppercase, lowercase and numbers"
        )
    ])
```

### Journalisation de Sécurité
```python
import logging

security_logger = logging.getLogger('security')

def log_security_event(event_type, details):
    security_logger.warning(f"Security Event: {event_type}", extra={
        'event_type': event_type,
        'ip_address': request.remote_addr,
        'user_agent': request.user_agent.string,
        'details': details
    })
```

### Session Management
```python
from flask_session import Session

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
Session(app)
```

## 🚨 Gestion des Incidents de Sécurité

### Détection des Intrusions
```python
def detect_suspicious_activity(request, user):
    suspicious = False
    if request.headers.get('User-Agent') not in user.known_user_agents:
        suspicious = True
    if request.remote_addr not in user.known_ips:
        suspicious = True
    
    if suspicious:
        log_security_event('suspicious_activity', {
            'user_id': user.id,
            'ip': request.remote_addr
        })
```

### Blocage Automatique
```python
def auto_block_ip(ip_address):
    failed_attempts = redis_client.incr(f"failed_login:{ip_address}")
    if failed_attempts > 5:
        redis_client.setex(f"blocked:{ip_address}", 3600, 1)
        log_security_event('ip_blocked', {'ip': ip_address})
```

## 📝 Checklist de Sécurité

### Déploiement
- [ ] Certificats SSL/TLS à jour
- [ ] Variables d'environnement sécurisées
- [ ] Ports non essentiels fermés
- [ ] Services mis à jour
- [ ] Sauvegardes chiffrées

### Application
- [ ] Validation des entrées
- [ ] Protection XSS/CSRF
- [ ] Rate limiting
- [ ] Logging sécurisé
- [ ] Authentification forte

### Base de données
- [ ] Accès restreint
- [ ] Sauvegardes régulières
- [ ] Données sensibles chiffrées
- [ ] Requêtes préparées
```
