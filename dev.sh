#!/bin/sh
cd `dirname $0`
docker-compose up -d dev-server
docker-compose exec dev-server ash
docker-compose down
