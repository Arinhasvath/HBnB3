# scripts/deploy.sh
#!/bin/bash

echo "Starting deployment..."

# Arrêt des conteneurs existants
docker-compose down

# Pull des dernières images
docker-compose pull

# Backup de la base avant déploiement
./backup_db.sh

# Démarrage des nouveaux conteneurs
docker-compose up -d

# Vérification de la santé
./scripts/healthcheck.sh

echo "Deployment complete!"