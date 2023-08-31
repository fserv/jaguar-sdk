#!/bin/sh

containerid=`docker ps -a |grep jaguardb|awk '{print $1}'`

docker stop --time=3600 $containerid

