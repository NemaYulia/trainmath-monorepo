#!/bin/bash

# TrainMath Deployment Script
set -e

echo "Starting TrainMath deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create logs directory
mkdir -p logs

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo "Please edit .env file with your production settings before running again."
    exit 1
fi

# Build and start services
echo "Building and starting services..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
docker-compose exec web python manage.py migrate

# Populate problem types
echo "Populating problem types..."
docker-compose exec web python manage.py populate_problem_types

# Create superuser (optional)
echo "Creating superuser..."
docker-compose exec web python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

# Collect static files
echo "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "Deployment completed successfully!"
echo "Application is available at: http://localhost"
echo "Admin panel: http://localhost/admin/"
echo "Admin dashboard: http://localhost/admin/dashboard/"

# Show logs
echo "Showing application logs..."
docker-compose logs -f web
