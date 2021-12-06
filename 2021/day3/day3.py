day = 3
filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
report = [n.split('\n')[0] for n in puzzle_input]

example = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010']
# report = example

bits = lambda i, iterable: [int(n[i]) for n in iterable]
most_common = lambda i, iterable: '1' if sum(bits(i, iterable)) >= len(list(iterable))/2 else '0'
least_common = lambda i, iterable: '0' if sum(bits(i, iterable)) >= len(list(iterable))/2 else '1'

bin_to_dec = lambda bin: sum([2**i * int(bin[-i-1]) for i in range(len(bin))])

remove = lambda i, fn, iterable: filter(lambda n: n[i] == fn(i, iterable), iterable)

def part_1():
  gamma_rate = ''.join([most_common(i, report) for i in range(len(report[0]))])
  epsilon_rate = ''.join([least_common(i, report) for i in range(len(report[0]))])
  return bin_to_dec(gamma_rate) * bin_to_dec(epsilon_rate)

def part_2():
  keep_most_common, keep_least_common = report, report
  for i in range(len(report[0])):
    temp_most = list(remove(i, most_common, keep_most_common))
    keep_most_common = temp_most if temp_most else keep_most_common

    temp_least = list(remove(i, least_common, keep_least_common))
    keep_least_common = temp_least if temp_least else keep_least_common
  
  return bin_to_dec(keep_most_common[0]) * bin_to_dec(keep_least_common[0])

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
