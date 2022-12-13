from __future__ import annotations

import ast
import functools
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def compare_packets(left: list[int] | int, right: list[int] | int) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        return -1 if left < right else 1
    if isinstance(left, list) and isinstance(right, list):
        for li, ri in zip(left, right):
            result = compare_packets(li, ri)
            if result != 0:
                return result

        if len(left) == len(right):
            return 0
        return -1 if len(left) < len(right) else 1
    if isinstance(left, int) and isinstance(right, list):
        return compare_packets([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare_packets(left, [right])
    return 0


def puzzle1(input_: str) -> int:
    indices = []
    for i, pair in enumerate(input_.split("\n\n"), start=1):
        left, right = (ast.literal_eval(p) for p in pair.splitlines())
        if compare_packets(left, right) < 0:
            indices.append(i)
    return sum(indices)


def puzzle2(input_: str) -> int:
    input_ = input_.replace("\n\n", "\n")
    packets = [ast.literal_eval(p) for p in input_.splitlines()]
    packets.extend([[[2]], [[6]]])
    packets.sort(key=functools.cmp_to_key(compare_packets))
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


INPUT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
EXPECTED_1 = 13  # 1, 2, 4, and 6
EXPECTED_2 = 140  # 10th and 14th


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
