#!/bin/bash

# Couleurs pour la lisibilité
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Test création d'un administrateur...${NC}"

# 1. Créer un utilisateur admin
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "admin123",
    "is_admin": true
}'

# 2. Login avec l'admin
echo -e "\n${GREEN}Login avec l'admin...${NC}"
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "admin@example.com",
    "password": "admin123"
}'
