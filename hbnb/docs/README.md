# HBNB - Clone Airbnb 🏠
![HBNB Logo](./assets/images/hbnb_logo.png)

## 📋 Table des Matières
- [Aperçu](#aperçu)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Documentation](#documentation)
- [Contribution](#contribution)
- [Licence](#licence)

## 🎯 Aperçu

HBNB est un clone d'Airbnb développé dans le cadre du projet Holberton. Cette application permet aux utilisateurs de :
- Créer un compte et se connecter
- Publier des annonces de logements
- Rechercher des logements
- Réserver des séjours
- Laisser des avis

## 🛠 Technologies Utilisées

### Backend
- Python 3.8+
- Flask (Framework Web)
- SQLAlchemy (ORM)
- MySQL (Base de données)

### Infrastructure
- Docker & Docker Compose
- Nginx (Reverse Proxy)
- Gunicorn (Serveur WSGI)

### Monitoring
- Prometheus
- Grafana

### Tests
- Pytest
- Locust (Tests de charge)

## 💻 Installation

### Prérequis
```bash
# Versions requises
Python 3.8+
Docker 20.10+
Docker Compose 2.0+
```

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/hbnb.git
cd hbnb
```

2. **Configurer l'environnement**
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
# Pour Linux/Mac :
source venv/bin/activate
# Pour Windows :
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

3. **Configuration**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer les variables d'environnement
nano .env
```

4. **Lancer avec Docker**
```bash
# Construire et démarrer les conteneurs
docker-compose up --build -d

# Vérifier les logs
docker-compose logs -f
```

## 🚀 Utilisation

### Interface Web
Accédez à l'application via : `http://localhost`

### API
Base URL : `http://localhost/api/v1`

Exemples de requêtes :
```bash
# Créer un utilisateur
curl -X POST http://localhost/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Lister les logements
curl http://localhost/api/v1/places
```

## 🧪 Tests

### Tests Unitaires
```bash
# Lancer tous les tests
python -m pytest

# Lancer tests spécifiques
python -m pytest tests/test_models/
```

### Tests de Charge
```bash
# Lancer les tests de charge
docker-compose -f docker-compose.load-test.yml up -d
# Accéder à l'interface Locust : http://localhost:8089
```

## 📚 Documentation

Documentation détaillée disponible dans le dossier `/docs` :
- [Documentation Technique](./docs/TECHNICAL.md)
- [Guide API](./docs/API.md)
- [Guide de Contribution](./docs/CONTRIBUTING.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](./docs/CONTRIBUTING.md) pour plus de détails.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- 🐛 [Ouvrir une issue](https://github.com/votre-username/hbnb/issues)
- 📧 Contact : votre-email@example.com

## 📊 Statut du Projet

![Tests Status](https://github.com/votre-username/hbnb/workflows/tests/badge.svg)
![Deploy Status](https://github.com/votre-username/hbnb/workflows/deploy/badge.svg)
```
