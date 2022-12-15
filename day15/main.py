from __future__ import annotations

import os
import re

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


TARGET_Y = 2_000_000
D_BEACON_RANGE = (0, 4_000_000)


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort()
    stack = []
    stack.append(intervals[0])

    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)

    return stack


def puzzle1(input_: str, target_y: int = TARGET_Y) -> int:
    grid = set()
    beacons = set()
    for line in input_.splitlines():
        sx, sy, bx, by = (int(m) for m in re.findall(r"[-\d]+", line))
        beacons.add((bx, by))
        dist = manhattan_distance(sx, sy, bx, by)

        if sy - dist <= target_y <= sy + dist:
            row_len = dist - abs(target_y - sy)
            for x in range(sx - row_len, sx + row_len + 1):
                grid.add((x, target_y))

    return len(grid - beacons)


def puzzle2(
    input_: str,
    beacon_range: tuple[int, int] = D_BEACON_RANGE,
) -> int:
    beacons = []
    sections = []
    dists = []

    for line in input_.splitlines():
        sx, sy, bx, by = (int(m) for m in re.findall(r"[-\d]+", line))
        sections.append((sx, sy))
        beacons.append((bx, by))
        dists.append(manhattan_distance(sx, sy, bx, by))

    for target_y in range(beacon_range[0], beacon_range[1] + 1):
        ranges = []

        for (sx, sy), (bx, by), dist in zip(sections, beacons, dists):
            if sy - dist <= target_y <= sy + dist:
                row_len = dist - abs(target_y - sy)

                lx = sx - row_len
                rx = sx + row_len

                if lx < beacon_range[0]:
                    lx = beacon_range[0]
                if lx > beacon_range[1]:
                    lx = beacon_range[1]
                if rx > beacon_range[1]:
                    rx = beacon_range[1]
                if rx < beacon_range[0]:
                    rx = beacon_range[0]

                ranges.append([lx, rx])

        intervals = merge(ranges)
        if len(intervals) == 2:
            x = intervals[0][1] + 1
            return x * D_BEACON_RANGE[1] + target_y
    return 0


INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
EXPECTED_1 = 26
EXPECTED_2 = 56000011


@pytest.mark.parametrize(
    ("input_", "expected", "puzzle", "extra"),
    (
        (INPUT, EXPECTED_1, puzzle1, 10),
        (INPUT, EXPECTED_2, puzzle2, (0, 20)),
    ),
)
def test_puzzle(input_, expected, puzzle, extra):
    assert puzzle(input_, extra) == expected


if __name__ == "__main__":
    input_ = read_input()
    print(puzzle1(input_))
    print(puzzle2(input_))
