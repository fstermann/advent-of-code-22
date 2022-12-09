from __future__ import annotations

import os
from itertools import product

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def puzzle1(input_: str) -> int:
    trees: dict[tuple[int, int], int] = {}

    for i, line in enumerate(input_.splitlines()):
        for j, t in enumerate(line):
            trees[(i, j)] = int(t)

    MAX_I, MAX_J = i, j

    vis_trees = set()

    for i in range(0, MAX_I + 1):
        vis_trees.add((i, 0))
        vis_trees.add((i, MAX_J))

        # from left
        highest = trees[(i, 0)]
        for j in range(1, MAX_J):
            if trees[(i, j)] > highest:
                highest = max(highest, trees[(i, j)])
                vis_trees.add((i, j))

        # from right
        highest = trees[(i, MAX_J)]
        for j in range(MAX_J - 1, -1, -1):
            if trees[(i, j)] > highest:
                highest = max(highest, trees[(i, j)])
                vis_trees.add((i, j))

    for j in range(0, MAX_J + 1):
        vis_trees.add((0, j))
        vis_trees.add((MAX_I, j))

        # from top
        highest = trees[(0, j)]
        for i in range(1, MAX_I):
            if trees[(i, j)] > highest:
                highest = max(highest, trees[(i, j)])
                vis_trees.add((i, j))

        # from bottom
        highest = trees[(MAX_I, j)]
        for i in range(MAX_I - 1, -1, -1):
            if trees[(i, j)] > highest:
                highest = max(highest, trees[(i, j)])
                vis_trees.add((i, j))

    return len(vis_trees)


def puzzle2(input_: str) -> int:
    trees: dict[tuple[int, int], int] = {}

    for i, line in enumerate(input_.splitlines()):
        for j, t in enumerate(line):
            trees[(i, j)] = int(t)

    MAX_I, MAX_J = i, j

    visions = []
    for i, j in product(range(1, MAX_I), range(1, MAX_J)):
        tree = trees[(i, j)]

        vis_bottom = 0
        for ki in range(i + 1, MAX_I + 1):
            vis_bottom += 1
            if trees[(ki, j)] >= tree:
                break

        vis_top = 0
        for ki in range(i - 1, -1, -1):
            vis_top += 1
            if trees[(ki, j)] >= tree:
                break

        vis_right = 0
        for kj in range(j + 1, MAX_J + 1):
            vis_right += 1
            if trees[(i, kj)] >= tree:
                break

        vis_left = 0
        for kj in range(j - 1, -1, -1):
            vis_left += 1
            if trees[(i, kj)] >= tree:
                break

        visions.append(vis_bottom * vis_top * vis_right * vis_left)

    return max(visions)


INPUT = """\
30373
25512
65332
33549
35390
"""
EXPECTED_1 = 21
EXPECTED_2 = 8


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
