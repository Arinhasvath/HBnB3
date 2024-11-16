# scripts/healthcheck.sh
#!/bin/bash

echo "Running health checks..."

# Vérification API
curl -f http://localhost/api/health || exit 1

# Vérification Base de données
docker-compose exec db mysqladmin ping -h localhost || exit 1

# Vérification Prometheus
curl -f http://localhost:9090/-/healthy || exit 1

echo "All health checks passed!"