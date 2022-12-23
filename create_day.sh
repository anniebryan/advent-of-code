#!/bin/bash
#
year=$1
day=$2
echo "creating files for day ${day} of year ${year}..."
mkdir ${year}
mkdir ${year}/day${day}
echo "############################\n# Advent of Code 2022 Day ${day}\n############################\n\ndef part_1(input):\n  return\n  \ndef part_2(input):\n  return\n\n\nday = ${day}\n\nwith open(f'day{day}/day{day}_ex.txt') as ex_filename:\n  example_input = [r.strip() for r in ex_filename.readlines()]\n  print(\"---Example---\")\n  print(f'Part 1: {part_1(example_input)}')\n  print(f'Part 2: {part_2(example_input)}')\n\nwith open(f'day{day}/day{day}.txt') as filename:\n  puzzle_input = [r.strip() for r in filename.readlines()]\n  print(\"---Puzzle---\")\n  print(f'Part 1: {part_1(puzzle_input)}')\n  print(f'Part 2: {part_2(puzzle_input)}')" >> ${year}/day${day}/day${day}.py
touch ${year}/day${day}/day${day}.txt
touch ${year}/day${day}/day${day}_ex.txt
echo "done"
