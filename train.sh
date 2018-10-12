#!/bin/bash

docker-compose kill && \
docker-compose rm -f && \
docker-compose -f docker-compose.yml -f docker-compose.train.yml up
