from __future__ import annotations

import itertools
import os
from typing import Generator

import pytest


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


WIDTH = 7
X_OFF = 2
Y_OFF = 3 + 1
MAX_ROCKS_1 = 2022
MAX_ROCKS_2 = 1_000_000_000_000

Rock = set[tuple[int, int]]


def is_valid_move(rock: Rock, chamber: set[tuple[int, int]]) -> bool:
    if any((x, y) in chamber for x, y in rock):
        return False
    if not all(x < WIDTH for x, _ in rock):
        return False
    if not all(x >= 0 for x, _ in rock):
        return False
    return True


def get_rocks(y) -> Generator[Rock, int, None]:
    rocks = [
        lambda y: {
            (X_OFF, y),
            (X_OFF + 1, y),
            (X_OFF + 2, y),
            (X_OFF + 3, y),
        },  # -
        lambda y: {
            (X_OFF + 1, y),
            (X_OFF, y + 1),
            (X_OFF + 1, y + 1),
            (X_OFF + 2, y + 1),
            (X_OFF + 1, y + 2),
        },  # +
        lambda y: {
            (X_OFF, y),
            (X_OFF + 1, y),
            (X_OFF + 2, y),
            (X_OFF + 2, y + 1),
            (X_OFF + 2, y + 2),
        },  # L
        lambda y: {
            (X_OFF, y),
            (X_OFF, y + 1),
            (X_OFF, y + 2),
            (X_OFF, y + 3),
        },  # |
        lambda y: {
            (X_OFF, y),
            (X_OFF + 1, y),
            (X_OFF, y + 1),
            (X_OFF + 1, y + 1),
        },  # []
    ]

    for rock in itertools.cycle(rocks):
        received = yield rock(y)  # a sent value will be assigned to 'received'
        y = y if received is None else received


def print_chamber(chamber: set[tuple[int, int]]) -> None:
    xs, ys = zip(*chamber)
    yr = range(max(ys), min(ys) - 1, -1)
    xr = range(min(xs), max(xs) + 1)
    for y in yr:
        print(f"{y:3}", end=" ")
        for x in xr:
            print("#" if (x, y) in chamber else ".", end="")
        print()


def move_rock(rock: Rock, x: int = 0, y: int = 0) -> Rock:
    return {(x + dx, y + dy) for dx, dy in rock}


def puzzle1(input_: str) -> int:
    chamber = {(x, 0) for x in range(WIDTH)}
    y = 0 + Y_OFF

    rocks = get_rocks(y)
    current_rock = next(rocks)

    input_ = input_.strip().replace("\n", "")
    moves = [1 if m == ">" else -1 for m in input_]

    n = 0

    for move in itertools.cycle(moves):
        # Move vertically
        moved_rock = move_rock(current_rock, x=move)
        if is_valid_move(moved_rock, chamber):
            current_rock = moved_rock

        # Move horizontally
        moved_rock = move_rock(current_rock, y=-1)
        if is_valid_move(moved_rock, chamber):
            current_rock = moved_rock
        else:
            # Rock settled
            chamber.update(current_rock)
            max_y = max(y for _, y in chamber)
            current_rock = rocks.send(max_y + Y_OFF)

            n += 1
            if n == MAX_ROCKS_1:
                break

    return max(y for _, y in chamber)


def puzzle2(input_: str) -> int:
    def clean_chamber(chamber):
        xs, ys = zip(*chamber)

    chamber = {(x, 0) for x in range(WIDTH)}
    y = 0 + Y_OFF

    rocks = get_rocks(y)
    current_rock = next(rocks)

    input_ = input_.strip().replace("\n", "")
    moves = [1 if m == ">" else -1 for m in input_]

    n = 0
    move_cycle = 0
    height_diff = 0
    rocks_diff = 0
    total_height = 0

    while n < MAX_ROCKS_2:
        move_cycle += 1
        height_before = max(y for _, y in chamber)
        rocks_before = n
        print("On move cycle", move_cycle)
        for move in moves:
            # Move vertically
            moved_rock = move_rock(current_rock, x=move)
            if is_valid_move(moved_rock, chamber):
                current_rock = moved_rock

            # Move horizontally
            move_rock(current_rock, y=-1)
            if is_valid_move(moved_rock, chamber):
                current_rock = moved_rock
            else:
                # Rock settled
                chamber.update(current_rock)
                max_y = max(y for _, y in chamber)
                current_rock = rocks.send(max_y + Y_OFF)

                n += 1
                if n == MAX_ROCKS_2:
                    break

        height_after = max(y for _, y in chamber)
        rocks_after = n

        if (
            height_after - height_before == height_diff
            and rocks_after - rocks_before == rocks_diff
        ):
            rocks_per_cycle = rocks_diff
            print("Pattern found")
            rocks_left_to_fill = MAX_ROCKS_2 - n
            print("Rocks left to fill", rocks_left_to_fill)
            move_cycles_left = rocks_left_to_fill // rocks_per_cycle
            n += move_cycles_left * rocks_per_cycle
            total_height += move_cycles_left * height_diff
            print("Only", MAX_ROCKS_2 - n, "rocks left to fill")

        height_diff = height_after - height_before
        total_height += height_diff
        print("Height diff", height_diff)

        rocks_diff = rocks_after - rocks_before
        print("Rocks diff", rocks_diff)
        print()
    return total_height


INPUT = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
EXPECTED_1 = 3068
EXPECTED_2 = 1514285714288


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
