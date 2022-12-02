import pytest


def read_input() -> str:
    with open("day01/input.txt", "r") as f:
        return f.read()


def puzzle1(input_: str) -> int:
    elves_calories = input_.split(sep="\n\n")
    return max(sum(int(cal) for cal in cals.splitlines()) for cals in elves_calories)


def puzzle2(input_: str) -> int:
    elves_calories = input_.split(sep="\n\n")
    return sum(
        sorted(sum(int(cal) for cal in cals.splitlines()) for cals in elves_calories)[
            -3:
        ]
    )


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
