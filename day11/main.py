from __future__ import annotations

import os
from math import lcm
from typing import Callable
from typing import NamedTuple

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


class Monkey(NamedTuple):
    items: list[int]
    operation: Callable[[int], int]
    test: int
    next_monkey: dict[bool, int]


def get_monkeys(input_: str) -> list[Monkey]:
    monkeys = []
    for monkey in input_.split("\n\n"):
        info = monkey.splitlines()[1:]
        starting_items = [int(i) for i in info[0].split(":")[1].split(", ")]
        operation = eval(f"lambda old: {info[1].split('=')[1].strip()}")
        test = int(info[2].split()[-1])
        if_true = int(info[3].split()[-1])
        if_false = int(info[4].split()[-1])
        monkeys.append(
            Monkey(
                starting_items,
                operation,
                test,
                {True: if_true, False: if_false},
            ),
        )
    return monkeys


def puzzle1(input_: str) -> int:
    monkeys = get_monkeys(input_)
    inspections = [0] * len(monkeys)

    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            for level in monkey.items.copy():
                # Inspect
                level = monkey.operation(level) // 3
                inspections[i] += 1
                # Throw
                next_monkey = monkey.next_monkey[level % monkey.test == 0]
                monkeys[next_monkey].items.append(level)
            monkey.items.clear()

    a1, a2 = sorted(inspections)[-2:]
    return a1 * a2


def puzzle2(input_: str) -> int:
    monkeys = get_monkeys(input_)
    inspections = [0] * len(monkeys)

    test_lcm = lcm(*[monkey.test for monkey in monkeys])

    for _ in range(10_000):
        for i, monkey in enumerate(monkeys):
            for level in monkey.items:
                # Inspect
                level = monkey.operation(level) % test_lcm
                inspections[i] += 1
                # Throw
                next_monkey = monkey.next_monkey[level % monkey.test == 0]
                monkeys[next_monkey].items.append(level)
            monkey.items.clear()

    a1, a2 = sorted(inspections)[-2:]
    return a1 * a2


INPUT = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED_1 = 10605
EXPECTED_2 = 2713310158


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
