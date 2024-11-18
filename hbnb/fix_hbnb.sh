#!/bin/bash

# 1. Remplacer l'importation de url_quote par quote
echo "Remplacement de l'importation de url_quote par quote..."
grep -rl "from urllib.parse import quote" . | xargs sed -i 's/from urllib.parse import quote/from urllib.parse import quote/g'

# 2. Créer le fichier tests/__init__.py s'il n'existe pas
if [ ! -f tests/__init__.py ]; then
    echo "Création du fichier tests/__init__.py..."
    touch tests/__init__.py
fi

# 3. Créer le fichier tests/base.py
echo "Création du fichier tests/base.py..."
cat <<EOL > tests/base.py
from flask_testing import TestCase
from app import create_app, db

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
EOL

# 4. Mettre à jour requirements.txt avec les versions compatibles
echo "Mise à jour de requirements.txt..."
cat <<EOL > requirements.txt
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
SQLAlchemy==2.0.20
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-Login==0.6.2
Flask-Bcrypt==1.0.1
Flask-WTF==1.1.1
Flask-RESTful==0.3.10
pytest==7.4.2
pytest-cov==4.1.0
pytest-flask==1.2.0
Pillow==10.0.0
boto3==1.28.36
redis==5.0.0
flask-caching==2.0.2
flask-cors==4.0.0
python-dotenv==1.0.0
prometheus-flask-exporter==0.22.4
email-validator==2.0.0
EOL

# 5. Installer les dépendances mises à jour
echo "Installation des dépendances mises à jour..."
pip install -r requirements.txt

# 6. Exécuter les tests après les modifications
echo "Exécution des tests..."
python -m pytest tests/ -v

echo "Script de correction terminé."