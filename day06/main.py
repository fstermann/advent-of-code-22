from __future__ import annotations

import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


PACKET_MARKER = 4
MESSAGE_MARKER = 14


def puzzle1(input_: str) -> int:
    for i in range(PACKET_MARKER, len(input_)):
        if len(set(input_[i - PACKET_MARKER : i])) == PACKET_MARKER:
            return i
    return -1


def puzzle2(input_: str) -> int:
    for i in range(MESSAGE_MARKER, len(input_)):
        if len(set(input_[i - MESSAGE_MARKER : i])) == MESSAGE_MARKER:
            return i
    return -1


INPUT = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
EXPECTED_1 = 7
EXPECTED_2 = 19


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
