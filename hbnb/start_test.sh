#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Initialisation environnement de test HBnB${NC}"

# Configuration de base
export API_URL="http://127.0.0.1:5000/api/v1"

# Création utilisateur standard
echo -e "\n${GREEN}1. Création utilisateur test${NC}"
curl -X POST "${API_URL}/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "test123",
    "is_admin": false
}'

# Création utilisateur admin
echo -e "\n${GREEN}2. Création utilisateur admin${NC}"
curl -X POST "${API_URL}/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "admin123",
    "is_admin": true
}'

# Obtention token utilisateur standard
echo -e "\n${GREEN}3. Obtention token utilisateur${NC}"
USER_RESPONSE=$(curl -s -X POST "${API_URL}/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "test123"
}')

# Obtention token admin
echo -e "\n${GREEN}4. Obtention token admin${NC}"
ADMIN_RESPONSE=$(curl -s -X POST "${API_URL}/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "admin@example.com",
    "password": "admin123"
}')

# Extraction et sauvegarde des tokens
USER_TOKEN=$(echo $USER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
ADMIN_TOKEN=$(echo $ADMIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Sauvegarde des variables
echo "export API_URL='${API_URL}'" > test_env.sh
echo "export TOKEN='${USER_TOKEN}'" >> test_env.sh
echo "export ADMIN_TOKEN='${ADMIN_TOKEN}'" >> test_env.sh

echo -e "\n${GREEN}Configuration terminée !${NC}"
echo "Variables sauvegardées dans test_env.sh"
echo "Pour utiliser : source test_env.sh"