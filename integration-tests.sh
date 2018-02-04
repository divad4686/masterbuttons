#!/bin/bash
set -e
docker-compose -f docker-compose.yml up --build -d
sleep 3s
docker-compose -f docker-compose.tests.yml up --build