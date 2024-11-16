# 🔍 Guide de Débogage HBNB

## 🐛 Problèmes Courants

### 1. Erreurs de Base de Données

#### Erreur de connexion
```bash
sqlalchemy.exc.OperationalError: MySQL Connection refused
```

**Solution:**
1. Vérifier que MySQL est en cours d'exécution
```bash
sudo service mysql status
```
2. Vérifier les credentials dans .env
3. Tester la connexion
```bash
mysql -u user -p
```

### 2. Erreurs d'Authentification

#### Token invalide
```python
# Vérifier la validité du token
from app.utils.auth import decode_token

try:
    decoded = decode_token(token)
except Exception as e:
    print(f"Erreur de token: {str(e)}")
```

### 3. Performance

#### Requêtes lentes
```python
# Activer le logging SQL
app.config['SQLALCHEMY_ECHO'] = True

# Utiliser explain pour analyser les requêtes
def debug_query(query):
    print(query.statement.compile(compile_kwargs={"literal_binds": True}))
```

## 🔧 Outils de Débogage

### Flask Debug Toolbar
```python
from flask_debugtoolbar import DebugToolbarExtension

app.config['DEBUG_TB_ENABLED'] = True
toolbar = DebugToolbarExtension(app)
```

### Logging Personnalisé
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.error("Error message")
```

## 🧪 Tests de Débogage

### Tests Unitaires
```python
def test_debug_example():
    with app.test_client() as client:
        response = client.get('/api/v1/places')
        print(response.get_json())  # Debug output
```

## 📊 Monitoring

### Prometheus Metrics
```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

### Healthchecks
```bash
curl http://localhost:5000/health
```
