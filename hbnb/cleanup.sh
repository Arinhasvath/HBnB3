#!/bin/bash
echo "Nettoyage des tests..."

# Garder uniquement la structure de base
mkdir -p tests/test_models
mkdir -p tests/test_api

# Supprimer tous les anciens tests
find tests/ -name "test_*.py" -type f -delete
find tests/ -type d -not -name "test_models" -not -name "test_api" -delete

echo "Nettoyage terminé."