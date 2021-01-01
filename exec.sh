#!/bin/sh
cd `dirname $0`
docker-compose up -d dev
docker-compose exec dev ash
docker-compose down
