#!/bin/bash

######################################################################
##
## This script setup virtual env, packages, and jaguardb server
##
######################################################################

### create virtual env
python3 -m venv simple_rag_venv 
source  simple_rag_venv/bin/activate


### install packages
 pip install -U Pillow
 pip install -U pyopenssl cryptography
 pip install -U sentence-transformers
 pip install -U jaguardb-http-client


### setup docker container of jaguardb servers
### You must already have docker installed on the host first.
sudo docker pull jaguardb/jaguardb_with_http
sudo docker run -d -p 8888:8888 -p 8080:8080 --name jaguardb_with_http jaguardb/jaguardb_with_http
