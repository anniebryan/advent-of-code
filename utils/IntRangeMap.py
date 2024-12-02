from .IntRangeSet import IntRangeSet

class IntRangeMap:
    all_maps: dict[tuple[str, str], "IntRangeMap"] = {}

    def __init__(self, source_type: str, dest_type: str):
        self.source_type = source_type
        self.dest_type = dest_type
        self.lines = []
        IntRangeMap.all_maps[(source_type, dest_type)] = self

    def add_line_to_map(self, line: str) -> None:
        dest_range_start, source_range_start, length = [int(n) for n in line.split()]
        self.lines.append((dest_range_start, source_range_start, length - 1))

    def apply_to_int_range(self, value_range: IntRangeSet) -> IntRangeSet:
        result = IntRangeSet()
        unmapped_range = value_range
        for map_dest_start, map_source_start, map_length in self.lines:
            map_source_range = IntRangeSet()
            map_source_range.add_range(map_source_start, map_length)

            intersect_range = IntRangeSet.intersection(unmapped_range, map_source_range)
            intersect_range.add_offset(map_dest_start - map_source_start)
            for start, length in intersect_range.ranges:
                result.add_range(start, length)

            unmapped_range = IntRangeSet.difference(unmapped_range, map_source_range)

        for start, length in unmapped_range.ranges:
            result.add_range(start, length)
        return result
