#!/bin/bash

function log() {
    echo ""
    echo "        $1"
    echo
}

./boatd-start test/config.yaml &
boatd_pid=$!

sleep 2

log "STARTED BOATD WITH PID=$boatd_pid"
log "TESTING GET..."

curl -i localhost:2222/heading && echo

curl -i localhost:2222/pony && echo

log "TESTING POST..."

curl -i -X POST -H "Content-Type: application/json" -d '{"quit": true}' http://localhost:2222
echo

sleep 2

if kill $boatd_pid 2> /dev/null; then
    log "FAILED TO STOP, KILLED BOATD";
else
    log "TESTS FINISHED";
fi
