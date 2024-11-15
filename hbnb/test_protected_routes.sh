#!/bin/bash

API_URL="http://127.0.0.1:5000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Obtenir un token d'authentification
echo -e "${GREEN}Obtention du token...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "test123"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
USER_ID=$(echo $LOGIN_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

echo -e "\n${GREEN}1. Test GET /users/ (Liste des utilisateurs)${NC}"
echo "=============================="
curl -X GET "$API_URL/users/" \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\n${GREEN}2. Test GET /users/{id} (Détails d'un utilisateur)${NC}"
echo "=============================="
curl -X GET "$API_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\n${GREEN}3. Test PUT /users/{id} (Mise à jour d'un utilisateur)${NC}"
echo "=============================="
curl -X PUT "$API_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "email": "john.updated@example.com"
  }'

echo -e "\n\n${GREEN}4. Test d'accès aux données d'un autre utilisateur (devrait échouer)${NC}"
echo "=============================="
curl -X GET "$API_URL/users/another-user-id" \
  -H "Authorization: Bearer $TOKEN"
  