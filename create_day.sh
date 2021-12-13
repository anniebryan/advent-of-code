#!/bin/bash
#
echo creating files for day $2 of year $1...
mkdir $1/day$2
echo -e "day = $2\n\nexample_filename = f'day{day}/day{day}_ex.txt'\nexample_input = open(example_filename).readlines()\n\nfilename = f'day{day}/day{day}.txt'\npuzzle_input = open(filename).readlines()\n\ndef part_1():\n  return\n\ndef part_2():\n  return\n\nprint(f'Part 1: {part_1()}')\nprint(f'Part 2: {part_2()}')" >>  $1/day$2/day$2.py
touch $1/day$2/day$2.txt
touch $1/day$2/day$2_ex.txt
echo done
