#!/bin/sh

if [ "$#" != "1" ] ; then
  echo "Usage: gpx2waypoints.sh <gpxfile>"
  echo "Where <gpxfile> is a GPX file created using OpenCPN's route export function and containing rtept points"
  exit 1
fi

#look for lines like
#<rtept lat="52.417712434" lon="-4.095229239">
#grab the numbers in the quotes and remove duplicate lines as opencpn has a habit of duplicating the last point
grep "rtept lat" $1 | awk -F\" '{print $2" "$4}' | uniq
