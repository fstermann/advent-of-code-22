import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT, "r") as f:
        return f.read()


def puzzle1(input_: str) -> int:
    pass


def puzzle2(input_: str) -> int:
    pass


INPUT = """\

"""
EXPECTED_1 = 0
EXPECTED_2 = 0


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
