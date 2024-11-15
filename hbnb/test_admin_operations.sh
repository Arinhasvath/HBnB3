#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Charger les variables d'environnement
source test_env.sh

echo -e "${GREEN}Tests des opérations administrateur${NC}"
echo "==========================================="

# 1. Test création d'amenity (admin seulement)
echo -e "\n${GREEN}1. Création d'une amenity${NC}"
AMENITY_RESPONSE=$(curl -s -X POST "${API_URL}/amenities/" \
-H "Authorization: Bearer ${ADMIN_TOKEN}" \
-H "Content-Type: application/json" \
-d '{
    "name": "Swimming Pool"
}')
echo "$AMENITY_RESPONSE"

# 2. Test modification d'un utilisateur par admin
echo -e "\n${GREEN}2. Modification d'un utilisateur${NC}"
USER_UPDATE_RESPONSE=$(curl -s -X PUT "${API_URL}/users/${USER_ID}" \
-H "Authorization: Bearer ${ADMIN_TOKEN}" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@example.com"
}')
echo "$USER_UPDATE_RESPONSE"

# 3. Test création d'un nouvel utilisateur par admin
echo -e "\n${GREEN}3. Création d'un nouvel utilisateur${NC}"
NEW_USER_RESPONSE=$(curl -s -X POST "${API_URL}/users/" \
-H "Authorization: Bearer ${ADMIN_TOKEN}" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "New",
    "last_name": "User",
    "email": "newuser@example.com",
    "password": "newpass123"
}')
echo "$NEW_USER_RESPONSE"
