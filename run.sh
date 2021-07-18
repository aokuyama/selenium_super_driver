#!/bin/sh
cd `dirname $0`
docker-compose run app python ${@:1}
