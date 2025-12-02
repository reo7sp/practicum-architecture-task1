#!/bin/bash
set -e

echo "Installing Python dependencies with Poetry..."

cd auth-service
poetry install
cd ..

cd devices-service
poetry install
cd ..

cd integration-service
poetry install
cd ..

cd automations-service
poetry install
cd ..

cd actions-service
poetry install
cd ..

echo "Downloading Go modules..."

cd sensors-service
go mod download
cd ..

cd api-gateway
go mod download
cd ..

echo "Setup completed successfully!"
