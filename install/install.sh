#!/bin/bash

set -e  # exit immediately on any error

TMPDIR=$(mktemp -d)

function cleanup() 
{
  echo "Cleaning up $TMPDIR"
  /bin/rm -rf "$TMPDIR"
}

trap cleanup EXIT


cd $TMPDIR

echo "Download jaguardb.tar.gz from http://jaguardb.com ..."
curl -ffSL 'http://jaguardb.com/jaguardb.tar.gz' -o jaguardb.tar.gz

echo "Extract jaguardb.tar.gz ..."
tar zxf jaguardb.tar.gz


echo "Start JaguarDB ..."
./install_jdb_http.sh


