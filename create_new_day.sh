#!/bin/bash

# Exit on error, unset variable, or pipeline failure
set -euo pipefail

# Check for required arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <year> <day>"
    exit 1
fi

# Variables
year=$1
day=$2
filename="aoc_${year}/day_${day}/solution.py"
directory="$(dirname "$filename")"

# Create directory if it doesn't exist
if [ ! -d "$directory" ]; then
    mkdir -p "$directory"
fi

# Create example and puzzle files if they don't exist
touch "$directory/example.txt" "$directory/puzzle.txt"

# Check if template.py exists
if [ ! -f "template.py" ]; then
    echo "Error: template.py not found."
    exit 1
fi

# Create solution file if it doesn't exist
if [ -f "$filename" ]; then
    echo "The file $filename already exists."
else
    echo "Creating files for day $day of year $year..."
    cp template.py "${filename}"
    sed -i "" "s/{{ year }}/$year/g; s/{{ day }}/$day/g" "$filename"
fi
