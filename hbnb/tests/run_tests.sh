#!/bin/bash

# Activation de l'environnement virtuel
source venv/bin/activate

# Installer les dépendances si nécessaire
pip install -r requirements.txt

# Lancer tous les tests avec couverture
python -m pytest \
    --verbose \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    tests/

# Vérifier si les tests ont réussi
if [ $? -eq 0 ]; then
    echo "✅ Tous les tests ont réussi!"
    echo "📊 Rapport de couverture généré dans htmlcov/"
else
    echo "❌ Certains tests ont échoué"
    exit 1
fi