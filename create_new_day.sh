#!/bin/bash

year=$1
day=$2

echo "Creating files for day ${day} of year ${year}..."

mkdir ${year}
mkdir ${year}/day${day}

python3 render_template.py template.j2 ${year} ${day} > ${year}/day${day}/solution.py

touch ${year}/day${day}/example.txt
touch ${year}/day${day}/puzzle.txt

echo "Done"
