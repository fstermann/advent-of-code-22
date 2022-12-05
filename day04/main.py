from __future__ import annotations

import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def puzzle1(input_: str) -> int:
    n = 0
    for line in input_.splitlines():
        e1, e2 = line.split(",")
        l1, l2 = (int(e) for e in e1.split("-"))
        ids1 = set(range(l1, l2 + 1))
        r1, r2 = (int(e) for e in e2.split("-"))
        ids2 = set(range(r1, r2 + 1))
        if len(ids1 - ids2) == 0 or len(ids2 - ids1) == 0:
            n += 1
    return n


def puzzle2(input_: str) -> int:
    n = 0
    for line in input_.splitlines():
        e1, e2 = line.split(",")
        l1, l2 = (int(e) for e in e1.split("-"))
        ids1 = set(range(l1, l2 + 1))
        r1, r2 = (int(e) for e in e2.split("-"))
        ids2 = set(range(r1, r2 + 1))
        if ids1 & ids2:
            n += 1
    return n


INPUT = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED_1 = 2
EXPECTED_2 = 4


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
