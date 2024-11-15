#!/bin/bash

# Couleurs pour la lisibilité
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Initialisation des tests HBNB${NC}"
echo "================================="

# Configuration
API_URL="http://127.0.0.1:5000/api/v1"

# 1. Créer l'utilisateur test
echo -e "\n${GREEN}1. Création utilisateur de test...${NC}"
CREATE_USER_RESPONSE=$(curl -s -X POST "${API_URL}/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "test123"
}')

echo "Réponse création utilisateur: $CREATE_USER_RESPONSE"

# 2. Login pour obtenir le token
echo -e "\n${GREEN}2. Obtention du token...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "test123"
}')

# Extraire le token
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}Token obtenu avec succès !${NC}"
    
    # Sauvegarder les variables pour réutilisation
    echo "export API_URL='${API_URL}'" > test_env.sh
    echo "export TOKEN='${TOKEN}'" >> test_env.sh
    
    echo -e "\nVariables d'environnement sauvegardées dans test_env.sh"
    echo "Pour les utiliser, faire: source test_env.sh"

    # Test rapide de validation
    echo -e "\n${GREEN}3. Test de validation du token...${NC}"
    curl -s -X GET "${API_URL}/users/" \
    -H "Authorization: Bearer ${TOKEN}"
else
    echo "Erreur: Impossible d'obtenir le token"
    echo "Réponse login: $LOGIN_RESPONSE"
fi