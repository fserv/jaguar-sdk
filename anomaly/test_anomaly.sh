#!/bin/bash

export PYTHONPATH=$HOME/jaguar/lib
export LD_LIBRARY_PATH=$HOME/jaguar/lib

python3 example_vector_anomaly.py 127.0.0.1 8888
