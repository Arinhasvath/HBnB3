# 📦 Guide de Déploiement HBNB

## 🚀 Déploiement en Production

### Prérequis Production
- Serveur Linux (Ubuntu 20.04+ recommandé)
- Docker & Docker Compose
- Nginx
- Certificat SSL (Let's Encrypt)
- Base de données MySQL

### 1. Configuration du Serveur

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade

# Installation des dépendances
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx


### 2. Structure des Dossiers Production
```bash
/opt/hbnb/
├── docker/
│   ├── nginx/
│   │   └── nginx.conf
│   └── docker-compose.prod.yml
├── .env.prod
└── scripts/
    ├── deploy.sh
    └── backup.sh
```

### 3. Configuration Nginx
```nginx
# /opt/hbnb/docker/nginx/nginx.conf
server {
    listen 80;
    server_name hbnb.com;

    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Script de Déploiement
```bash
#!/bin/bash
# /opt/hbnb/scripts/deploy.sh

echo "📦 Déploiement HBNB..."

# Pull dernières modifications
git pull origin main

# Construction des conteneurs
docker-compose -f docker-compose.prod.yml build

# Redémarrage des services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

echo "✅ Déploiement terminé!"
```
Je continue `deployment.md` :

```markdown
### 5. Configuration Base de Données Production

```bash
# /opt/hbnb/.env.prod
DB_HOST=db
DB_NAME=hbnb_prod
DB_USER=hbnb_user
DB_PASSWORD=secure_password
```

### 6. Docker Compose Production
```yaml
# /opt/hbnb/docker/docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: 
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - FLASK_ENV=production
    depends_on:
      - db
    networks:
      - hbnb_network

  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
      - MYSQL_DATABASE=${DB_NAME}
      - MYSQL_USER=${DB_USER}
      - MYSQL_PASSWORD=${DB_PASSWORD}
    networks:
      - hbnb_network

networks:
  hbnb_network:

volumes:
  mysql_data:
```

### 7. SSL avec Let's Encrypt
```bash
# Installation du certificat SSL
sudo certbot --nginx -d hbnb.com -d www.hbnb.com

# Renouvellement automatique
sudo certbot renew --dry-run
```

### 8. Monitoring Production

```yaml
# /opt/hbnb/docker/docker-compose.prod.yml (ajout services monitoring)
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus:/etc/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
```

### 9. Sauvegardes Automatiques
```bash
#!/bin/bash
# /opt/hbnb/scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/hbnb/backups"

# Backup base de données
docker exec hbnb_db_1 mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Compression
gzip $BACKUP_DIR/db_$DATE.sql

# Nettoyage des vieux backups (garde 7 jours)
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
```

### 10. Checklist Déploiement

✅ **Avant Déploiement**
- [ ] Tests passés
- [ ] Variables d'environnement configurées
- [ ] Sauvegardes à jour
- [ ] DNS configuré

🚀 **Pendant Déploiement**
- [ ] Maintenance mode ON
- [ ] Backup base de données
- [ ] Déploiement code
- [ ] Migrations base de données
- [ ] Tests smoke
- [ ] Maintenance mode OFF

📝 **Après Déploiement**
- [ ] Vérifier logs
- [ ] Vérifier métriques
- [ ] Tester fonctionnalités critiques

### 11. Rollback Procédure

```bash
#!/bin/bash
# /opt/hbnb/scripts/rollback.sh

VERSION=$1

if [ -z "$VERSION" ]
then
    echo "❌ Version de rollback requise"
    exit 1
fi

echo "⏪ Rollback vers version $VERSION"

# Restaurer version précédente
git checkout $VERSION

# Rebuilder et redémarrer
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

echo "✅ Rollback terminé"
```

### 12. Troubleshooting Production

**Problèmes Courants et Solutions:**

1. **Application Inaccessible**
```bash
# Vérifier status services
docker-compose -f docker-compose.prod.yml ps

# Vérifier logs
docker-compose -f docker-compose.prod.yml logs web
```

2. **Erreurs Base de Données**
```bash
# Vérifier connexion
docker exec -it hbnb_db_1 mysql -u root -p

# Vérifier migrations
flask db current
flask db history
```
