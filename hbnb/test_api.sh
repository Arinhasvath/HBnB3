#!/bin/bash

# Configuration
API_URL="http://127.0.0.1:5000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}1. Obtention du token...${NC}"
TOKEN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

if [ -z "$TOKEN" ]
then
    echo -e "${RED}Échec de l'obtention du token${NC}"
    exit 1
fi

echo -e "${GREEN}Token obtenu avec succès${NC}"

echo -e "\n${GREEN}2. Test des routes protégées${NC}"

# Test GET /users/
echo -e "\n${GREEN}Liste des utilisateurs:${NC}"
curl -s -X GET "$API_URL/users/" \
  -H "Authorization: Bearer $TOKEN"

# Test GET /users/{id}
echo -e "\n${GREEN}Détails d'un utilisateur:${NC}"
curl -s -X GET "$API_URL/users/[user_id]" \
  -H "Authorization: Bearer $TOKEN"

# Test PUT /users/{id}
echo -e "\n${GREEN}Mise à jour d'un utilisateur:${NC}"
curl -s -X PUT "$API_URL/users/[user_id]" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "test@example.com"
  }'

# Test sans token (devrait échouer)
echo -e "\n${GREEN}Test sans token (devrait échouer):${NC}"
curl -s -X GET "$API_URL/users/"

# Test avec token invalide (devrait échouer)
echo -e "\n${GREEN}Test avec token invalide (devrait échouer):${NC}"
curl -s -X GET "$API_URL/users/" \
  -H "Authorization: Bearer invalid_token"