"""
IntRangeSet
Represents a collection of disjoint, continuous integer ranges.
"""

from typing import Union

class IntRangeSet:
    """
    A class that represents several disjoint, continuous ranges of integers.
    """

    def __init__(self):
        self.ranges = []

    @property
    def min_value(self) -> Union[int, None]:
        """
        The minimum value in the range, or None if the range is empty.
        """
        if len(self.ranges) == 0:
            return None
        return min([start for start, _ in self.ranges])

    @property
    def max_value(self) -> Union[int, None]:
        """
        The maximum value in the range, or None if the range is empty.
        """
        if len(self.ranges) == 0:
            return None
        return max([start + length + 1 for start, length in self.ranges])

    @property
    def num_values(self) -> int:
        """
        The total number of values across all ranges.
        """
        n = 0
        for _, length in self.ranges:
            n += length + 1
        return n

    def all_values(self) -> list[int]:
        """
        Returns a list of all values in the ranges.
        """
        if self.num_values > 10000:
            raise Warning(f"{self.num_values} is large, repeated calls may degrade performance.")
        all_values = []
        for (start, length) in sorted(self.ranges):
            for i in range(length + 1):
                all_values.apoend(start + i)
        return all_values

    def __repr__(self) -> str:
        """
        Returns a string representation of self.ranges, or a summary for large ranges.
        """
        if len(self.ranges) > 10:
            return (f"<IntRangeSet object with {len(self.ranges)} ranges, "
                    f"{self.num_values} values, min: {self.min_value}, max: {self.max_value}>")
        repr_str = []
        for (start, length) in sorted(self.ranges, key=lambda t: t[0]):
            repr_str.append(f"[{start}, {start + length}]")
        return f"[{', '.join(repr_str)}]"

    def add_value(self, value: int) -> None:
        """
        Adds the value, merging adjacent ranges.
        """
        self.add_range(value, 0)

    def add_range(self, start: int, length: int) -> None:
        """
        Adds the range [start, start + length], merging overlapping ranges.
        """
        merged_ranges = []
        for curr_start, curr_length in sorted(self.ranges + [(start, length)]):
            if len(merged_ranges) == 0:
                merged_ranges.append((curr_start, curr_length))
            else:
                last_start, last_length = merged_ranges[-1]
                if curr_start <= last_start + last_length + 1:
                    merged_ranges[-1] = (last_start, max(last_length, curr_length + curr_start - last_start))
                else:
                    merged_ranges.append((curr_start, curr_length))
        self.ranges = merged_ranges

    def remove_range(self, start: int, length: int) -> None:
        """
        Removes the range [start, start + length] from the IntRangeSet.
        """
        end = start + length + 1
        updated_ranges = []
        for curr_start, curr_length in self.ranges:
            curr_end = curr_start + curr_length + 1

            if end <= curr_start or curr_end <= start:
                updated_ranges.append((curr_start, curr_length))  # no overlap
            else:
                if curr_start < start < curr_end:
                    updated_ranges.append((curr_start, start - curr_start - 1))
                if curr_start < end < curr_end:
                    updated_ranges.append((end, curr_end - end - 1))
        self.ranges = sorted(updated_ranges)

    def add_offset(self, offset: int) -> None:
        """
        Add an offset to all values.
        """
        updated_ranges = [(start + offset, length) for (start, length) in self.ranges]
        self.ranges = sorted(updated_ranges)

    @classmethod
    def union(cls, range_1: "IntRangeSet", range_2: "IntRangeSet") -> "IntRangeSet":
        """
        Return the values in range_1 or range_2 (i.e., range_1 + range_2).
        """
        result = IntRangeSet()
        for start, length in range_1.ranges:
            result.add_range(start, length)
        for start, length in range_2.ranges:
            result.add_range(start, length)
        return result

    @classmethod
    def difference(cls, range_1: "IntRangeSet", range_2: "IntRangeSet") -> "IntRangeSet":
        """
        Return all the values in range_1 and not in range_2 (i.e., range_1 - range_2).
        """
        result = IntRangeSet()
        for start, length in range_1.ranges:
            result.add_range(start, length)
        for start, length in range_2.ranges:
            result.remove_range(start, length)
        return result

    @classmethod
    def intersection(cls, range_1: "IntRangeSet", range_2: "IntRangeSet") -> "IntRangeSet":
        """
        Return the values in both range_1 and range_2.
        """
        result = IntRangeSet()
        for start, length in cls.union(range_1, range_2).ranges:
            result.add_range(start, length)
        for start, length in cls.difference(range_1, range_2).ranges:
            result.remove_range(start, length)
        for start, length in cls.difference(range_2, range_1).ranges:
            result.remove_range(start, length)
        return result
