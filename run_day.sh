#!/bin/bash
#
year=$1
day=$2
echo "running code for day ${day} of year ${year}..."
cd ${year}
python3 day${day}/day${day}.py
