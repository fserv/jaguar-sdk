#!/bin/bash

##############################################################
## command to start jaguardb in docker container
##
##  sudo ./jaguardb_start_in_docker.sh
##
##############################################################

echo docker run -d -it -p 8888:8888 jaguardb/jaguardb:latest
docker run -d -it -p 8888:8888 --name jaguardb jaguardb/jaguardb:latest
