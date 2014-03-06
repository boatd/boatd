#!/bin/bash

./boatd-start test/config.yaml &
boatd_pid=$!

sleep 1

echo
echo "        TESTING GET..."
echo

curl -v localhost:2222/heading && echo

curl localhost:2222/pony && echo

kill $boatd_pid
