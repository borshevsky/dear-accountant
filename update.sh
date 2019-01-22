#!/bin/sh

set -e

docker kill `docker ps --filter ancestor=telegram-accountant -q` > /dev/null 2>&1 ||:
docker build -t telegram-accountant -f docker/Dockerfile .
docker run -it -d --env-file env telegram-accountant
