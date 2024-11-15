#!/bin/bash

# Configuration
API_URL="http://127.0.0.1:5000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Tests d'authentification HBnB${NC}"
echo "================================"

# 1. Test de création d'utilisateur
echo -e "\n${GREEN}1. Création d'un utilisateur${NC}"
curl -X POST "$API_URL/users/" \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User"
}'

# 2. Test de login avec les credentials corrects
echo -e "\n\n${GREEN}2. Login avec credentials corrects${NC}"
LOGIN_RESPONSE=$(curl -X POST "$API_URL/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "test123"
}')

# Extraire et stocker le token
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo -e "\nToken reçu: $TOKEN"

# 3. Test de login avec mauvais credentials
echo -e "\n${GREEN}3. Login avec mauvais credentials${NC}"
curl -X POST "$API_URL/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "wrongpass"
}'

# 4. Test d'accès protégé avec token valide
echo -e "\n\n${GREEN}4. Accès route protégée avec token valide${NC}"
curl -X GET "$API_URL/users/" \
-H "Authorization: Bearer $TOKEN"

# 5. Test d'accès protégé sans token
echo -e "\n\n${GREEN}5. Accès route protégée sans token${NC}"
curl -X GET "$API_URL/users/"

# 6. Test d'accès protégé avec token invalide
echo -e "\n\n${GREEN}6. Accès route protégée avec token invalide${NC}"
curl -X GET "$API_URL/users/" \
-H "Authorization: Bearer invalid_token"

# 7. Test de revalidation du token
echo -e "\n\n${GREEN}7. Retest login après précédents tests${NC}"
curl -X POST "$API_URL/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "password": "test123"
}'

echo -e "\n\n${GREEN}Tests terminés${NC}"