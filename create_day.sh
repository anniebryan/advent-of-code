#!/bin/bash
#
year=$1
day=$2
echo "creating files for day ${day} of year ${year}..."
mkdir ${year}
mkdir ${year}/day${day}
echo "day = ${day}\n\nexample_filename = f'day{day}/day{day}_ex.txt'\nexample_input = open(example_filename).readlines()\n\nfilename = f'day{day}/day{day}.txt'\npuzzle_input = open(filename).readlines()\n\ndef part_1(input):\n  return\n\ndef part_2(input):\n  return\n\nprint(f'Part 1 example: {part_1(example_input)}')\nprint(f'Part 1 puzzle: {part_1(puzzle_input)}')\n\nprint(f'Part 2 example: {part_2(example_input)}')\nprint(f'Part 2 puzzle: {part_2(puzzle_input)}')" >> ${year}/day${day}/day${day}.py
touch ${year}/day${day}/day${day}.txt
touch ${year}/day${day}/day${day}_ex.txt
echo "done"
