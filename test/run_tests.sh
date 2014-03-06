#!/bin/bash

./boatd-start &
boatd_pid=$!

echo "boatd started"

sleep 1

kill $boatd_pid
