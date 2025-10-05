#!/bin/bash

# TrainMath Backup Script
set -e

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="trainmath_backup_${DATE}.sql"

echo "Starting backup process..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running inside Docker container..."
    # Backup database
    pg_dump -h db -U trainmath -d trainmath > "/app/$BACKUP_DIR/$BACKUP_FILE"
else
    echo "Running on host system..."
    # Check if docker-compose is running
    if docker-compose ps | grep -q "Up"; then
        echo "Backing up database from Docker container..."
        docker-compose exec -T db pg_dump -U trainmath -d trainmath > "$BACKUP_DIR/$BACKUP_FILE"
    else
        echo "Docker containers are not running. Please start them first."
        exit 1
    fi
fi

# Compress backup
echo "Compressing backup..."
gzip "$BACKUP_DIR/$BACKUP_FILE"

# Remove backups older than 30 days
echo "Cleaning up old backups..."
find $BACKUP_DIR -name "trainmath_backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/$BACKUP_FILE.gz"

# Show backup size
ls -lh "$BACKUP_DIR/$BACKUP_FILE.gz"
