#!/bin/bash

./boatd-start test/config.yaml &
boatd_pid=$!

sleep 1

kill $boatd_pid
