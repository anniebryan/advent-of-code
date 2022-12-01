#!/bin/bash
#
echo creating files for day $2 of year $1...
mkdir $1
mkdir $1/day$2
echo "day = $2\n\nexample_filename = f'day{day}/day{day}_ex.txt'\nexample_input = open(example_filename).readlines()\n\nfilename = f'day{day}/day{day}.txt'\npuzzle_input = open(filename).readlines()\n\ndef part_1(input):\n  return\n\ndef part_2(input):\n  return\n\nprint(f'Part 1 example: {part_1(example_input)}')\nprint(f'Part 1 puzzle: {part_1(puzzle_input)}')\n\nprint(f'Part 2 example: {part_2(example_input)}')\nprint(f'Part 2 puzzle: {part_2(puzzle_input)}')" >>  $1/day$2/day$2.py
touch $1/day$2/day$2.txt
touch $1/day$2/day$2_ex.txt
echo done
