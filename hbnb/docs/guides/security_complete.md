# 🔐 Guide de Sécurité Complet HBNB

## 📋 Table des Matières
1. Authentication & Autorisation
2. Sécurité des Données
3. Protection API
4. Sécurité Infrastructure
5. Monitoring & Alertes
6. Gestion des Incidents
7. Conformité & RGPD

## 🔒 Authentication & Autorisation

### JWT Configuration
```python
JWT_CONFIG = {
    'SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
    'REFRESH_TOKEN_EXPIRES': timedelta(days=30),
    'BLACKLIST_ENABLED': True,
    'BLACKLIST_TOKEN_CHECKS': ['access', 'refresh']
}

class SecurityService:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

    def generate_tokens(self, user_id: str) -> dict:
        """Génère les tokens d'accès et de rafraîchissement."""
        access_token = create_access_token(
            identity=user_id,
            expires_delta=JWT_CONFIG['ACCESS_TOKEN_EXPIRES']
        )
        
        refresh_token = create_refresh_token(
            identity=user_id,
            expires_delta=JWT_CONFIG['REFRESH_TOKEN_EXPIRES']
        )
        
        # Stockage du refresh token
        self.redis.setex(
            f"refresh_token:{refresh_token}",
            JWT_CONFIG['REFRESH_TOKEN_EXPIRES'].total_seconds(),
            user_id
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': JWT_CONFIG['ACCESS_TOKEN_EXPIRES'].total_seconds()
        }

    def verify_token(self, token: str) -> dict:
        """Vérifie la validité d'un token."""
        try:
            # Vérifier si le token est blacklisté
            if self.redis.get(f"blacklist:{token}"):
                raise TokenBlacklistedError()
                
            payload = jwt.decode(
                token,
                JWT_CONFIG['SECRET_KEY'],
                algorithms=[JWT_CONFIG['ALGORITHM']]
            )
            
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    def blacklist_token(self, token: str):
        """Ajoute un token à la blacklist."""
        try:
            payload = self.verify_token(token)
            exp = datetime.fromtimestamp(payload['exp']) - datetime.utcnow()
            self.redis.setex(
                f"blacklist:{token}",
                exp.total_seconds(),
                '1'
            )
        except Exception as e:
            logger.error(f"Error blacklisting token: {str(e)}")
```

### Password Security
```python
class PasswordService:
    def __init__(self):
        self.bcrypt = Bcrypt()
        
    def hash_password(self, password: str) -> str:
        """Hash le mot de passe."""
        return self.bcrypt.generate_password_hash(
            password,
            rounds=12
        ).decode('utf-8')
        
    def verify_password(self, password: str, hashed: str) -> bool:
        """Vérifie le mot de passe."""
        return self.bcrypt.check_password_hash(hashed, password)
        
    def validate_password_strength(self, password: str) -> bool:
        """Valide la force du mot de passe."""
        if len(password) < 8:
            return False
            
        if not re.search(r"[A-Z]", password):
            return False
            
        if not re.search(r"[a-z]", password):
            return False
            
        if not re.search(r"[0-9]", password):
            return False
            
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
            
        return True

    def generate_reset_token(self, user_id: str) -> str:
        """Génère un token de réinitialisation."""
        token = secrets.token_urlsafe(32)
        self.redis.setex(
            f"reset_token:{token}",
            3600,  # 1 heure
            user_id
        )
        return token
```

### Sessions Management
```python
class SessionService:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        
    def create_session(self, user_id: str, device_info: dict) -> str:
        """Crée une nouvelle session."""
        session_id = str(uuid.uuid4())
        session_data = {
            'user_id': user_id,
            'device_info': device_info,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat()
        }
        
        self.redis.hmset(f"session:{session_id}", session_data)
        self.redis.expire(f"session:{session_id}", 86400)  # 24 heures
        
        return session_id
        
    def validate_session(self, session_id: str) -> bool:
        """Valide une session."""
        session = self.redis.hgetall(f"session:{session_id}")
        if not session:
            return False
            
        # Mettre à jour dernière activité
        self.redis.hset(
            f"session:{session_id}",
            'last_activity',
            datetime.utcnow().isoformat()
        )
        
        return True
        
    def invalidate_session(self, session_id: str):
        """Invalide une session."""
        self.redis.delete(f"session:{session_id}")
```

## 🔒 Sécurité des Données

### Encryption Service
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionService:
    def __init__(self):
        self.key = self._derive_key()
        self.fernet = Fernet(self.key)
        
    def _derive_key(self) -> bytes:
        """Dérive une clé de chiffrement."""
        salt = os.environ.get('ENCRYPTION_SALT').encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(os.environ.get('ENCRYPTION_KEY').encode())
        )
        return key
        
    def encrypt_data(self, data: str) -> str:
        """Chiffre des données."""
        return self.fernet.encrypt(data.encode()).decode()
        
    def decrypt_data(self, encrypted: str) -> str:
        """Déchiffre des données."""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Data Masking
```python
class DataMaskingService:
    @staticmethod
    def mask_email(email: str) -> str:
        """Masque une adresse email."""
        username, domain = email.split('@')
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
        return f"{masked_username}@{domain}"
        
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Masque un numéro de téléphone."""
        return '*' * (len(phone) - 4) + phone[-4:]
        
    @staticmethod
    def mask_card(card_number: str) -> str:
        """Masque un numéro de carte."""
        return '*' * 12 + card_number[-4:]
```

## 🛡️ Protection API

### Rate Limiting
```python
class RateLimiter:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        
    def is_allowed(self, key: str, limit: int, period: int) -> bool:
        """Vérifie si la requête est autorisée."""
        current = self.redis.get(key)
        
        if not current:
            self.redis.setex(key, period, 1)
            return True
            
        if int(current) >= limit:
            return False
            
        self.redis.incr(key)
        return True
        
    def get_remaining(self, key: str, limit: int) -> int:
        """Obtient le nombre de requêtes restantes."""
        current = self.redis.get(key)
        if not current:
            return limit
        return limit - int(current)
```

### Request Validation
```python
class RequestValidator:
    @staticmethod
    def validate_json(schema: dict):
        """Valide le JSON de la requête."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    jsonschema.validate(request.json, schema)
                except jsonschema.exceptions.ValidationError as e:
                    return jsonify({
                        'error': 'Invalid input',
                        'message': str(e)
                    }), 400
                return f(*args, **kwargs)
            return decorated_function
        return decorator
        
    @staticmethod
    def sanitize_input(data: str) -> str:
        """Nettoie les entrées utilisateur."""
        return bleach.clean(data)
```

## 🔍 Monitoring & Alertes

### Security Events
```python
class SecurityMonitor:
    def __init__(self):
        self.elastic = Elasticsearch([ES_HOST])
        
    def log_security_event(self, event_type: str, details: dict):
        """Enregistre un événement de sécurité."""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': event_type,
            'details': details,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        
        self.elastic.index(
            index='security-events',
            body=event
        )
        
    def detect_suspicious_activity(self, user_id: str):
        """Détecte une activité suspecte."""
        # Vérifier les tentatives de connexion échouées
        failed_attempts = self.redis.get(f"failed_login:{user_id}")
        if failed_attempts and int(failed_attempts) > 5:
            self.trigger_alert('excessive_login_attempts', {
                'user_id': user_id,
                'attempts': failed_attempts
            })
```

### Alert System
```python
class AlertSystem:
    def __init__(self):
        self.slack_webhook = os.environ.get('SLACK_WEBHOOK')
        
    def trigger_alert(self, alert_type: str, details: dict):
        """Déclenche une alerte."""
        alert = {
            'type': alert_type,
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Notification Slack
        requests.post(
            self.slack_webhook,
            json={'text': f"🚨 Security Alert: {alert_type}\n```{json.dumps(details, indent=2)}```"}
        )
        
        # Email aux administrateurs
        if alert_type in ['breach_attempt', 'data_leak']:
            self.notify_admins(alert)
```

## 📋 Conformité & RGPD

### Data Retention
```python
class DataRetentionService:
    def cleanup_old_data(self):
        """Nettoie les anciennes données."""
        # Supprimer les logs plus vieux que 90 jours
        cutoff = datetime.utcnow() - timedelta(days=90)
        Log.query.filter(Log.created_at < cutoff).delete()
        
        # Anonymiser les anciennes transactions
        Transaction.query.filter(
            Transaction.created_at < cutoff,
            Transaction.anonymized == False
        ).update({
            'card_number': None,
            'anonymized': True
        })
        
        db.session.commit()
        
    def handle_deletion_request(self, user_id: str):
        """Gère une demande de suppression RGPD."""
        user = User.query.get(user_id)
        if not user:
            return
            
        # Anonymiser les données
        user.email = f"deleted_user_{user_id}"
        user.phone = None
        user.address = None
        user.deleted_at = datetime.utcnow()
        
        db.session.commit()
```

## 🚨 Incident Response

### Incident Handler
```python
class IncidentHandler:
    def __init__(self):
        self.alert_system = AlertSystem()
        
    def handle_security_incident(self, incident_type: str, details: dict):
        """Gère un incident de sécurité."""
        # Logger l'incident
        logging.critical(f"Security Incident: {incident_type}", extra=details)
        
        # Alerter l'équipe
        self.alert_system.trigger_alert(incident_type, details)
        
        # Actions automatiques
        if incident_type == 'brute_force_attempt':
            self.block_ip(details['ip_address'])
        elif incident_type == 'data_breach':
            self.initiate_lockdown()
            
    def initiate_lockdown(self):
        """Initie un verrouillage de sécurité."""
        # Révoquer tous les tokens
        self.security_service.revoke_all_tokens()
        
        # Forcer la réinitialisation des mots de passe
        User.query.update({User.force_password_reset: True})
        
        db.session.commit()
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
