#!/bin/sh

while true
do
  echo $(date +%s)
  wget http://housing.gatech.edu/rooms/FreeRooms.json -O logs/$(date +%s).json
  echo "waiting 600 seconds"
  sleep 600
done