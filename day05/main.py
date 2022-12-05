from __future__ import annotations

import os
import re

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def puzzle1(input_: str) -> str:
    crate_config, moves = input_.split("\n\n")
    crate_stacks = crate_config.splitlines()[::-1]

    pos = [i for i, c in enumerate(crate_stacks[0]) if c != " "]
    crates: list[list[str]] = [[] for _ in pos]

    for line in crate_stacks[1:]:
        for i, p in enumerate(pos):
            crates[i] += [line[p]] if line[p] != " " else []

    for move in moves.splitlines():
        n, from_, to_ = (int(m) for m in re.findall(r"[0-9]+", move))
        cargo = crates[from_ - 1][-n:][::-1]
        crates[from_ - 1] = crates[from_ - 1][:-n]
        crates[to_ - 1] += cargo

    return "".join([c[-1] for c in crates])


def puzzle2(input_: str) -> str:
    crate_config, moves = input_.split("\n\n")
    crate_stacks = crate_config.splitlines()[::-1]

    pos = [i for i, c in enumerate(crate_stacks[0]) if c != " "]
    crates: list[list[str]] = [[] for _ in pos]

    for line in crate_stacks[1:]:
        for i, p in enumerate(pos):
            crates[i] += [line[p]] if line[p] != " " else []

    for move in moves.splitlines():
        n, from_, to_ = (int(m) for m in re.findall(r"[0-9]+", move))
        cargo = crates[from_ - 1][-n:]
        crates[from_ - 1] = crates[from_ - 1][:-n]
        crates[to_ - 1] += cargo

    return "".join([c[-1] for c in crates])


INPUT = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED_1 = "CMZ"
EXPECTED_2 = "MCD"


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
