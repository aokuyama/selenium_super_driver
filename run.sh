#!/bin/sh
cd `dirname $0`
docker-compose run selenium python ${@:1}
