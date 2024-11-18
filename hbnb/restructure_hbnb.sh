#!/bin/bash

# Créer la nouvelle structure de dossiers
mkdir -p app/{api/v1,models,repositories,services}
mkdir -p config
mkdir -p tests/{api,unit}
mkdir -p scripts

# Déplacer les fichiers vers les nouveaux emplacements
mv app/api/v1/* app/api/v1/
mv app/models/* app/models/
mv app/repositories/* app/repositories/
mv app/services/* app/services/
mv app/db.py app/
mv config.py config/settings.py

# Déplacer les tests
mv tests/api/* tests/api/
mv tests/unit/* tests/unit/

# Déplacer les scripts SQL
mv app/database/*.sql scripts/

# Nettoyer les dossiers vides
find . -type d -empty -delete

# Remplacer l'importation de url_quote
find . -type f -name "*.py" -exec sed -i 's/from werkzeug.urls import url_quote/from urllib.parse import quote as url_quote/g' {} +

# Créer un fichier .env à la racine du projet
touch .env

# Mettre à jour le fichier requirements.txt
cat > requirements.txt << EOL
Flask==2.3.3
Werkzeug==2.3.7
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

echo "Restructuration terminée. Veuillez vérifier les modifications et ajuster si nécessaire."