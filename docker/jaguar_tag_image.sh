#!/bin/bash


tag=$1

if [[ "x$tag" = "x" ]]; then
	echo "$0 <tag>"
	echo "$0 3.3.4"
	exit 1
fi


imageid=`docker images |grep jaguardb| awk '{print $3}'`
echo image id is $imageid
docker tag $imageid jaguardb/jaguardb:$tag
