from __future__ import annotations

import os
import string

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


item2priority = {s: p for p, s in enumerate(string.ascii_letters, start=1)}


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def puzzle1(input_: str) -> int:
    dups = []
    for s in input_.splitlines():
        r1, r2 = set(s[: len(s) // 2]), set(s[len(s) // 2 :])
        dups += list(r1 & r2)

    return sum(item2priority[d] for d in dups)


def puzzle2(input_: str) -> int:
    badges = []
    groups = input_.splitlines()
    for i in range(0, len(groups), 3):
        r1, r2, r3 = (set(g) for g in groups[i : i + 3])
        badges += list(r1 & r2 & r3)

    return sum(item2priority[b] for b in badges)


INPUT = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
EXPECTED_1 = 157
EXPECTED_2 = 70


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
