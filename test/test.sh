#!/bin/sh

mkdir -p output
ulimit -c unlimited

date
echo "Test unit.sql ..."
./jagdb -t main -v < unit.sql > output/unit.out
date

echo "Test vector.sql ..."
./jagdb -t main -v < vector.sql > output/vector.out
date


echo "Test time.sql ..."
./jagdb -t main -v < time.sql > output/time.out
date

echo "Test geo.sql ..."
./jagdb -t main -v < geo.sql > output/geo.out
date

echo "Test iot.sql ..."
./jagdb -t main -v < iot.sql > output/iot.out
date


echo "FAIL: "
grep FAIL output/unit.out output/time.out output/geo.out output/iot.out

echo "PASS: "
grep PASS output/unit.out output/time.out output/geo.out output/iot.out | wc -l

