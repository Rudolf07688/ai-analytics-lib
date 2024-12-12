#!/bin/bash

# Check if .env file exists, if not create from template
if [ ! -f .env ]; then
    echo "Creating .env file from .env.docker template..."
    cp .env.docker .env
    echo "Please edit .env file with your credentials before running again."
    exit 1
fi

# Build and start the containers
docker-compose up --build