#!/bin/bash

# Couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages de succès/échec
print_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} $1"
    else
        echo -e "${RED}[FAIL]${NC} $1"
        FAILED=1
    fi
}

# Initialiser la variable d'échec
FAILED=0

# 1. Vérifier l'installation des dépendances
echo "1. Vérification des dépendances..."
pip install -r requirements.txt
print_result "Installation des dépendances"

# 2. Lancer les tests unitaires
echo "2. Exécution des tests unitaires..."
python -m pytest tests/unit
print_result "Tests unitaires"

# 3. Lancer les tests d'API
echo "3. Exécution des tests d'API..."
python -m pytest tests/api
print_result "Tests API"

# 4. Vérifier la couverture du code
echo "4. Vérification de la couverture du code..."
coverage run -m pytest tests/
coverage report -m
print_result "Couverture du code"

# 5. Vérifier le style du code (PEP8)
echo "5. Vérification du style du code (PEP8)..."
flake8 .
print_result "Style du code (PEP8)"

# 6. Vérifier la présence des fichiers essentiels
echo "6. Vérification des fichiers essentiels..."
essential_files=("run.py" "config.py" "requirements.txt" "README.md")
for file in "${essential_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}[OK]${NC} $file existe"
    else
        echo -e "${RED}[FAIL]${NC} $file manquant"
        FAILED=1
    fi
done

# 7. Vérifier la structure du projet
echo "7. Vérification de la structure du projet..."
directories=("app" "tests" "migrations")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}[OK]${NC} Le répertoire $dir existe"
    else
        echo -e "${RED}[FAIL]${NC} Le répertoire $dir manquant"
        FAILED=1
    fi
done

# Résultat final
if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}Tous les tests ont réussi. Votre projet HBNB semble prêt pour l'évaluation!${NC}"
else
    echo -e "\n${RED}Certains tests ont échoué. Veuillez corriger les erreurs avant de soumettre votre projet.${NC}"
fi

exit $FAILED