from __future__ import annotations

import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def puzzle1(input_: str) -> int:
    elves = input_.split(sep="\n\n")
    return max(sum(map(int, cals.splitlines())) for cals in elves)


def puzzle2(input_: str) -> int:
    elves = input_.split(sep="\n\n")
    cals_ordered = sorted(sum(map(int, cals.splitlines())) for cals in elves)
    return sum(cals_ordered[-3:])


INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
EXPECTED_1 = 24000
EXPECTED_2 = 45000


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
