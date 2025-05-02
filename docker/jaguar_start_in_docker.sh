#!/bin/bash

##############################################################
## command to start jaguardb in docker container
##
##  sudo ./jaguardb_start_in_docker.sh
##
##############################################################

echo docker run -d -p 8080:8080 -p 8888:8888 jaguardb/jaguardb
docker run -d -p 8080:8080 -p 8888:8888 --name jaguardb jaguardb/jaguardb
