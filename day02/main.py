import pytest


def read_input() -> str:
    with open("day02/input.txt", "r") as f:
        return f.read()


shape2score = {"R": 1, "P": 2, "S": 3}
shape2win = {"R": "S", "P": "R", "S": "P"}
shape2lose = {v: k for k, v in shape2win.items()}
result2score = {"X": 0, "Y": 3, "Z": 6}


def puzzle1(input_: str) -> int:
    in2shape = {"A": "R", "B": "P", "C": "S", "X": "R", "Y": "P", "Z": "S"}

    for in_, shape in in2shape.items():
        input_ = input_.replace(in_, shape)

    rounds = [r.split(" ") for r in input_.splitlines()]

    total = 0
    for opp, you in rounds:
        total += shape2score[you]

        if opp == you:
            total += 3
        elif shape2win[opp] != you:
            total += 6

    return total


def puzzle2(input_: str) -> int:
    in2shape = {"A": "R", "B": "P", "C": "S"}

    for in_, shape in in2shape.items():
        input_ = input_.replace(in_, shape)

    in2shape.update({"X": "R", "Y": "P", "Z": "S"})

    rounds = [r.split(" ") for r in input_.splitlines()]

    total = 0
    for opp, you in rounds:
        total += result2score[you]

        if you == "X":
            total += shape2score[shape2win[opp]]
        elif you == "Y":
            total += shape2score[opp]
        else:
            total += shape2score[shape2lose[opp]]
    return total


INPUT = """\
A Y
B X
C Z
"""
EXPECTED_1 = 15
EXPECTED_2 = 12


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
