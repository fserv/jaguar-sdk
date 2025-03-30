#!/bin/sh

pd=`pwd -P`
tar zxf jaguar.tar.gz
cd jaguar-*
./install.sh
cd $pd
tar zxf fwww.tar.gz
cd fwww_*
./install.sh
