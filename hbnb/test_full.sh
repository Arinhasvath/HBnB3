#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

API_URL="http://127.0.0.1:5000/api/v1"

# Fonction de nettoyage
cleanup() {
    echo -e "${GREEN}Nettoyage de l'environnement de test...${NC}"
    curl -s -X DELETE "$API_URL/users/" # Exemple : ajustez selon votre endpoint de suppression
}

# Fonction pour vérifier le succès d'une requête
check_success() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}Erreur: $1${NC}"
        exit 1
    fi
}

echo -e "${GREEN}=== Tests Complets HBNB ===${NC}"

# Nettoyage initial
cleanup

# 1. Tests Authentification
echo -e "\n${GREEN}1. Login des utilisateurs${NC}"
USER_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "password": "test123"}')

check_success "Échec de connexion de l'utilisateur standard"
echo "User Response: $USER_RESPONSE"

ADMIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "admin@example.com",
    "password": "admin123"
}')
check_success "Échec de connexion de l'administrateur"
echo "Admin Response: $ADMIN_RESPONSE"

USER_TOKEN=$(echo $USER_RESPONSE | jq -r '.access_token // empty')
ADMIN_TOKEN=$(echo $ADMIN_RESPONSE | jq -r '.access_token // empty')

if [ -z "$USER_TOKEN" ] || [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}Erreur: Impossible d'obtenir les tokens${NC}"
    exit 1
fi

# 2. Test Place avec utilisateur standard
echo -e "\n${GREEN}2. Test création place${NC}"
PLACE_RESPONSE=$(curl -s -X POST "$API_URL/places/" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Test Place",
    "description": "Nice place for testing",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522
}')
check_success "Échec de création de la place"
echo "Place Response: $PLACE_RESPONSE"

PLACE_ID=$(echo $PLACE_RESPONSE | jq -r '.id // empty')
echo "Place créée avec ID: $PLACE_ID"

if [ -z "$PLACE_ID" ]; then
    echo -e "${RED}Erreur: Impossible d'obtenir l'ID de la place${NC}"
    exit 1
fi

# 3. Test Review avec second utilisateur
echo -e "\n${GREEN}3. Test Review avec second utilisateur${NC}"
SECOND_USER_RESPONSE=$(curl -s -X POST "$API_URL/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Second",
    "last_name": "User",
    "email": "second@example.com",
    "password": "test123"
}')
check_success "Échec de création du second utilisateur"
echo "Second User Response: $SECOND_USER_RESPONSE"

SECOND_TOKEN=$(curl -s -X POST "$API_URL/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "second@example.com",
    "password": "test123"
}' | jq -r '.access_token // empty')
check_success "Échec de connexion du second utilisateur"

REVIEW_RESPONSE=$(curl -s -X POST "$API_URL/reviews/" \
-H "Authorization: Bearer $SECOND_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "'$PLACE_ID'"
}')
check_success "Échec de création de la review"
echo "Review Response: $REVIEW_RESPONSE"

# Test Review avec utilisateur original
echo -e "\n${GREEN}Test Review avec utilisateur original${NC}"
ORIGINAL_USER_REVIEW_RESPONSE=$(curl -s -X POST "$API_URL/reviews/" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "'$PLACE_ID'"
}')
echo "Original User Review Response: $ORIGINAL_USER_REVIEW_RESPONSE"

# 4. Tests Admin
echo -e "\n${GREEN}4. Test modifications admin${NC}"
ADMIN_UPDATE_RESPONSE=$(curl -s -X PUT "$API_URL/places/$PLACE_ID" \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Updated by Admin",
    "price": 150.0
}')
check_success "Échec de modification de la place par l'admin"
echo "Admin Update Response: $ADMIN_UPDATE_RESPONSE"

# Sauvegarder les variables
echo "export API_URL='$API_URL'" > test_env.sh
echo "export USER_TOKEN='$USER_TOKEN'" >> test_env.sh
echo "export ADMIN_TOKEN='$ADMIN_TOKEN'" >> test_env.sh
echo "export PLACE_ID='$PLACE_ID'" >> test_env.sh

echo -e "\n${GREEN}Tests terminés. Variables sauvegardées${NC}"
