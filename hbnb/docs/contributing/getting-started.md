# 🚀 Guide de Démarrage Rapide HBNB

## 📋 Prérequis
- Python 3.8+
- Docker & Docker Compose
- Git
- MySQL (local ou Docker)

## 🔧 Installation

1. **Cloner le projet**
```bash
git clone https://github.com/your-username/hbnb.git
cd hbnb
```

2. **Configuration de l'environnement**
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt
```

3. **Configuration de la base de données**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer les variables d'environnement
DATABASE_URL=mysql://user:password@localhost/hbnb
```

4. **Lancer l'application**
```bash
# Avec Docker
docker-compose up -d

# Sans Docker
flask run
```

## 🖥️ Premier Pas

1. **Créer un utilisateur**
```python
from app.models import User
from app.db import db

user = User(
    email="test@example.com",
    password="password123",
    first_name="Test",
    last_name="User"
)

db.session.add(user)
db.session.commit()
```

2. **Créer un logement**
```python
from app.models import Place

place = Place(
    title="Bel appartement",
    price=100.00,
    owner_id=user.id
)

db.session.add(place)
db.session.commit()
```

## 📚 Ressources Additionnelles
- Documentation API complète
- Guide des tests
- Guide de déploiement
