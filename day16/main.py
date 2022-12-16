from __future__ import annotations

import collections
import itertools
import os
import re
from typing import NamedTuple

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


TOTAL_TIME = 30
reg = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)",
)


class Valve(NamedTuple):
    name: str
    flow_rate: int
    tunnels: list[str]


class BFS:
    graph: dict[str, list[str]]
    cache: dict[str, dict[str, list[str]]]

    def __init__(self, graph: dict[str, list[str]]):
        self.graph = graph
        self.cache = {}

    def bfs(self, start: str) -> dict[str, list[str]]:
        if start in self.cache:
            return self.cache[start]
        paths = bfs(self.graph, start)
        self.cache[start] = paths
        return paths


def bfs(graph: dict[str, list[str]], start: str) -> dict[str, list[str]]:
    q = collections.deque([start])
    explored = set()
    explored.add(start)

    paths: dict[str, list[str]] = {start: []}

    while q:
        v = q.popleft()
        for w in graph[v]:
            if w not in explored:
                paths[w] = paths[v] + [w]
                explored.add(w)
                q.append(w)
    return paths


def puzzle1(input_: str) -> int:
    valves = {}
    for line in input_.splitlines():
        matches = reg.match(line)
        assert matches is not None
        name, flow_rate, tunnels = matches.groups()
        valves[name] = Valve(name, int(flow_rate), tunnels.split(", "))

    graph = {v.name: v.tunnels for v in valves.values()}
    legit_valves = {v.name for v in valves.values() if v.flow_rate > 0}

    bfs_class = BFS(graph)

    def open_valve(
        valve_name: str,
        previous_valve: str,
        time_left: int,
        opened_valves: set[str],
        score: int = 0,
    ) -> int:
        paths = bfs_class.bfs(previous_valve)
        steps = len(paths[valve_name])

        time_left_on_arrival = time_left - steps
        if time_left_on_arrival <= 0:
            return score

        profit = time_left_on_arrival * valves[valve_name].flow_rate
        score += profit

        opened_valves.add(valve_name)
        paths = bfs_class.bfs(valve_name)

        remaing_valves = legit_valves - opened_valves
        if not remaing_valves:
            return score

        scores = []
        for valve in remaing_valves:
            scores.append(
                open_valve(
                    valve_name=valve,
                    previous_valve=valve_name,
                    time_left=time_left_on_arrival - 1,
                    opened_valves=opened_valves.copy(),
                    score=score,
                ),
            )
        return max(scores)

    scores = []
    for valve in legit_valves:
        scores.append(open_valve(valve, "AA", TOTAL_TIME - 1, set()))

    return max(scores)


def puzzle2(input_: str) -> int:
    all_valves = {}
    for line in input_.splitlines():
        matches = reg.match(line)
        assert matches is not None
        name, flow_rate, tunnels = matches.groups()
        all_valves[name] = Valve(name, int(flow_rate), tunnels.split(", "))

    graph = {v.name: v.tunnels for v in all_valves.values()}
    legit_valves = {v.name for v in all_valves.values() if v.flow_rate > 0}

    def move_to_valves(
        valve_names: tuple[str | None, str | None],
        graph,
        previous_valves: tuple[str | None, str | None],
        time_left: tuple[int, int],
        opened_valves: set[str],
        score: int = 0,
    ) -> int:
        valve_me = valve_names[0]
        valve_elephant = valve_names[1]

        # Me steps
        if valve_me is not None:
            paths_me = graph.bfs(previous_valves[0])
            steps_me = len(paths_me[valve_me])
            time_left_me = time_left[0] - steps_me
            if time_left_me > 0:
                profit_me = time_left_me * all_valves[valve_me].flow_rate
                score += profit_me
                opened_valves.add(valve_me)
                paths_me = graph.bfs(valve_me)
        else:
            time_left_me = -1

        # Elephant steps
        if valve_elephant is not None:
            paths_elephant = graph.bfs(previous_valves[1])
            steps_elephant = len(paths_elephant[valve_elephant])
            time_left_elephant = time_left[1] - steps_elephant
            if time_left_elephant > 0:
                profit_elephant = (
                    time_left_elephant * all_valves[valve_elephant].flow_rate
                )
                score += profit_elephant
                opened_valves.add(valve_elephant)
                paths_elephant = graph.bfs(valve_elephant)
        else:
            time_left_elephant = -1

        if time_left_me <= 0 and time_left_elephant <= 0:
            return score

        remaing_valves = legit_valves - opened_valves
        if not remaing_valves:
            return score

        scores = []
        remainders: itertools.product[tuple[str | None, str | None]]
        if time_left_me <= 0:
            remainders = itertools.product([None], remaing_valves)
        elif time_left_elephant <= 0:
            remainders = itertools.product(remaing_valves, [None])
        else:
            remainders = itertools.product(remaing_valves, remaing_valves)

        for valves in remainders:
            if valves[0] == valves[1]:
                continue

            scores.append(
                move_to_valves(
                    valve_names=valves,
                    previous_valves=(valve_me, valve_elephant),
                    graph=graph,
                    time_left=(time_left_me - 1, time_left_elephant - 1),
                    opened_valves=opened_valves.copy(),
                    score=score,
                ),
            )
        return max(scores)

    scores = []
    bfs_class = BFS(graph)

    for valves in itertools.product(legit_valves, legit_valves):
        if valves[0] == valves[1]:
            continue
        print("Starting with", valves)
        scores.append(
            move_to_valves(
                valve_names=valves,
                previous_valves=("AA", "AA"),
                graph=bfs_class,
                time_left=(TOTAL_TIME - 4 - 1, TOTAL_TIME - 4 - 1),
                opened_valves=set(),
            ),
        )

    return max(scores)


INPUT = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
EXPECTED_1 = 1651
EXPECTED_2 = 1707


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
