#!/bin/bash
# Définit que c'est un script bash

# Définition des variables
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")  # Crée un timestamp unique (ex: 20241114_143022)
BACKUP_DIR="/backups"                # Dossier où seront stockés les backups
MYSQL_USER="root"                    # Utilisateur MySQL
MYSQL_PASSWORD="root"                # Mot de passe MySQL
MYSQL_DATABASE="hbnb"                # Nom de la base de données

# Création du backup
# docker exec hbnb_db_1 : Exécute la commande dans le conteneur de la base de données
# mysqldump : Outil MySQL pour créer une sauvegarde
# > $BACKUP_DIR/hbnb_$TIMESTAMP.sql : Sauvegarde dans un fichier avec le timestamp
docker exec hbnb_db_1 mysqldump -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > $BACKUP_DIR/hbnb_$TIMESTAMP.sql

# Compression du fichier backup avec gzip
gzip $BACKUP_DIR/hbnb_$TIMESTAMP.sql

# Supprime les backups de plus de 7 jours
# find : cherche les fichiers
# -name "hbnb_*.sql.gz" : tous les fichiers backup compressés
# -mtime +7 : modifiés il y a plus de 7 jours
# -delete : les supprime
find $BACKUP_DIR -name "hbnb_*.sql.gz" -mtime +7 -delete