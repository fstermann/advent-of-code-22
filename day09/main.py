from __future__ import annotations

import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def euclidean_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def sign(x: tuple[int, ...]) -> tuple[int, ...]:
    return tuple({x_ < 0: -1, x_ > 0: 1, x_ == 0: 0}[True] for x_ in x)


def take_step(coord: tuple[int, int], direction: str) -> tuple[int, int]:
    if direction == "R":
        return coord[0] + 1, coord[1]
    elif direction == "L":
        return coord[0] - 1, coord[1]
    elif direction == "U":
        return coord[0], coord[1] + 1
    elif direction == "D":
        return coord[0], coord[1] - 1
    else:
        raise ValueError(f"Unknown direction: {direction}")


def move_closer(h: tuple[int, int], t: tuple[int, int]) -> tuple[int, int]:
    direction = sign((h[0] - t[0], h[1] - t[1]))
    return t[0] + direction[0], t[1] + direction[1]


def puzzle1(input_: str) -> int:
    h, t = (0, 0), (0, 0)
    t_pos = {t}

    for line in input_.splitlines():
        direction, n = line[0], int(line[1:])
        for _ in range(n):
            h = take_step(h, direction)
            if euclidean_distance(h, t) >= 2:
                t = move_closer(h, t)
            t_pos.add(t)

    return len(t_pos)


def puzzle2(input_: str) -> int:
    rope = [(0, 0)] * 10
    t_pos = {rope[-1]}

    for line in input_.splitlines():
        direction, n = line[0], int(line[1:])
        for _ in range(n):
            rope[0] = take_step(rope[0], direction)
            for i in range(len(rope) - 1):
                if euclidean_distance(rope[i], rope[i + 1]) >= 2:
                    rope[i + 1] = move_closer(rope[i], rope[i + 1])
            t_pos.add(rope[-1])

    return len(t_pos)


def print_grid(positions: set[tuple[int, int]], nums: bool = False) -> None:
    grid_x = max(
        abs(min(positions, key=lambda x: x[0])[0]),
        abs(max(positions, key=lambda x: x[0])[0]),
    )
    grid_x_range = list(range(-grid_x - 1, grid_x + 1))
    grid_y = max(
        abs(min(positions, key=lambda x: x[1])[1]),
        abs(max(positions, key=lambda x: x[1])[1]),
    )
    grid_y_range = list(range(-grid_y - 1, grid_y + 1))

    grid = {x: {y: "." for y in grid_y_range} for x in grid_x_range}

    for i, (x, y) in enumerate(positions):
        grid[x][y] = "#" if not nums else str(i)
    grid[0][0] = "s"

    print()
    for y in reversed(grid_y_range):
        print(f"{y:3}", end=" ")
        for x in grid_x_range:
            print(grid[x][y], end="")
        print()


INPUT = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED_1 = 88
EXPECTED_2 = 36


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
