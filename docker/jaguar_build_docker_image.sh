#!/bin/bash

######################################################3
##  Command to build docker image of jaguardb
##
##  sudo ./build_jaguar_docker_image.sh <version>
##  sudo ./build_jaguar_docker_image.sh 3.3.4
##
######################################################3

ver=$1

if [[ "x$ver" = "x" ]]; then
	echo "$0  <ver>"
	echo "Example  $0  3.3.4"
	exit 1
fi

# first place all jaguar files under /docker/releasedir/
docker build -t jaguardb:$ver   /docker

