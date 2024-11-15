#!/bin/bash

# Couleurs pour meilleure lisibilité
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== HBnB API Tests ===${NC}"

# 1. Initialisation
echo -e "\n${BLUE}1. Initialisation de l'environnement${NC}"
./start_test.sh
source test_env.sh

# 2. Tests Utilisateurs standard
echo -e "\n${BLUE}2. Tests des opérations utilisateur standard${NC}"
curl -X POST "${API_URL}/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "user@example.com",
    "password": "test123"
}'

# 3. Tests Admin
echo -e "\n${BLUE}3. Tests des opérations admin${NC}"
./test_admin_endpoints.sh

# 4. Tests Places
echo -e "\n${BLUE}4. Tests des opérations sur les places${NC}"
curl -X POST "${API_URL}/places/" \
-H "Authorization: Bearer ${TOKEN}" \
-H "Content-Type: application/json" \
-d '{
    "title": "Test Place",
    "description": "A test place",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522
}'

# 5. Tests Reviews
echo -e "\n${BLUE}5. Tests des opérations sur les reviews${NC}"
curl -X POST "${API_URL}/reviews/" \
-H "Authorization: Bearer ${TOKEN}" \
-H "Content-Type: application/json" \
-d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "PLACE_ID"
}'

echo -e "\n${GREEN}Tests terminés${NC}"
