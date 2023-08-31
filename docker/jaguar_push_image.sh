#!/bin/bash


tag=$1


if [[ "x$tag" = "x" ]]; then
        echo "$0 <tag>"
        echo "$0 3.3.4"
        exit 1
fi

echo "you must first:   docker login"

docker push jaguardb/jaguardb:$tag

