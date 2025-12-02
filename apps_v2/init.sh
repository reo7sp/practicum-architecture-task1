#!/bin/bash
set -e

echo "Starting the Smart Home Microservices..."
echo "Building and starting containers..."
docker-compose up --build -d

echo "Waiting for services to be ready..."

for i in {1..30}; do
  if docker exec sensors-postgres pg_isready -U postgres > /dev/null 2>&1 && \
     docker exec devices-postgres pg_isready -U postgres > /dev/null 2>&1 && \
     docker exec integrations-postgres pg_isready -U postgres > /dev/null 2>&1 && \
     docker exec auth-postgres pg_isready -U postgres > /dev/null 2>&1 && \
     docker exec automations-postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "All PostgreSQL instances are ready!"
    break
  fi
  echo "Waiting for PostgreSQL instances to start... ($i/30)"
  sleep 1
done

if ! docker exec sensors-postgres pg_isready -U postgres > /dev/null 2>&1 || \
   ! docker exec devices-postgres pg_isready -U postgres > /dev/null 2>&1 || \
   ! docker exec integrations-postgres pg_isready -U postgres > /dev/null 2>&1 || \
   ! docker exec auth-postgres pg_isready -U postgres > /dev/null 2>&1 || \
   ! docker exec automations-postgres pg_isready -U postgres > /dev/null 2>&1; then
  echo "Error: Some PostgreSQL instances did not start within the expected time."
  exit 1
fi

echo "All services are up and running!"
echo "The API Gateway is available at http://localhost:8080"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop the services, run: docker-compose down"
