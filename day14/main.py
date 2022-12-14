from __future__ import annotations

import os

import pytest


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


SAND_START = (500, 0)


def build_cave(input_: str):
    all_positions = []
    for line in input_.splitlines():
        pos_raw = line.split(" -> ")
        positions = [tuple(map(int, pos.split(","))) for pos in pos_raw]
        all_positions.append(positions)

    xs, ys = zip(*[pos for positions in all_positions for pos in positions])
    yr = range(0, max(ys) + 1)
    cave = {(x, y): "." for x in range(min(xs), max(xs) + 1) for y in yr}

    for positions in all_positions:
        for i in range(len(positions) - 1):
            pos1, pos2 = positions[i], positions[i + 1]
            xr = range(min(pos1[0], pos2[0]), max(pos1[0], pos2[0]) + 1)
            yr = range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1]) + 1)
            for x in xr:
                for y in yr:
                    cave[x, y] = "#"

    return cave


def print_cave(cave):
    xs, ys = zip(*cave.keys())
    yr = range(min(ys), max(ys) + 1)
    xr = range(min(xs), max(xs) + 1)
    print(
        "    " + "".join(["v" if x == 500 else " " for x in xr]),
    )
    for y in yr:
        print(f"{y:3}", end=" ")
        for x in xr:
            print(cave.get((x, y), "."), end="")
        print()


def puzzle1(input_: str) -> int:
    cave = build_cave(input_)

    bottom = False
    n = 0
    while not bottom:
        n += 1
        x, y = SAND_START
        while True:
            y += 1
            if bottom := (x, y) not in cave:
                break

            if cave[x, y] == ".":
                continue

            x -= 1
            if bottom := (x, y) not in cave:
                break
            if cave[x, y] == ".":
                continue

            x += 2
            if bottom := (x, y) not in cave:
                break

            if cave[x, y] != ".":
                cave[x - 1, y - 1] = "o"
                break

    return n - 1


def puzzle2(input_: str) -> int:
    cave = build_cave(input_)
    max_y = max(y for _, y in cave.keys()) + 2

    n = 0
    while True:
        n += 1
        x, y = SAND_START
        while True:
            y += 1

            if y + 1 == max_y:
                # Create safety net
                cave[(x - 2, max_y)] = "#"
                cave[(x - 1, max_y)] = "#"
                cave[(x, max_y)] = "#"
                cave[(x + 1, max_y)] = "#"
                cave[(x + 2, max_y)] = "#"

            if cave.get((x, y), ".") == ".":
                continue

            x -= 1
            if cave.get((x, y), ".") == ".":
                continue

            x += 2
            if cave.get((x, y), ".") != ".":
                x, y = x - 1, y - 1
                cave[x, y] = "o"
                break

        if (x, y) == SAND_START:
            break

    return n


INPUT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED_1 = 24
EXPECTED_2 = 93


@pytest.mark.parametrize(
    ("input_", "expected", "puzzle"),
    (
        (INPUT, EXPECTED_1, puzzle1),
        (INPUT, EXPECTED_2, puzzle2),
    ),
)
def test_puzzle(input_, expected, puzzle):
    assert puzzle(input_) == expected


if __name__ == "__main__":
    input_ = read_input()
    print(puzzle1(input_))
    print(puzzle2(input_))
