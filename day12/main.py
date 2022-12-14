from __future__ import annotations

import collections
import os
import string

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

Coord = tuple[int, int]

charmap = {c: i for i, c in enumerate(string.ascii_lowercase)}
charmap.update({"S": 0, "E": 25})


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


def bfs(graph: dict[Coord, list[Coord]], start: Coord) -> dict[Coord, int]:
    q = collections.deque([start])
    explored = set()
    explored.add(start)
    distances = {start: 0}

    while q:
        v = q.popleft()
        for w in graph[v]:
            if w not in explored:
                distances[w] = distances[v] + 1
                explored.add(w)
                q.append(w)
    return distances


def get_heightmap(input_: str) -> tuple[dict[Coord, int], Coord, Coord]:
    heightmap: dict[Coord, int] = {}
    start = end = None
    for i, line in enumerate(input_.splitlines()):
        for j, c in enumerate(line):
            heightmap[(i, j)] = charmap[c]
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
    assert start is not None
    assert end is not None
    return heightmap, start, end


def get_adjacent_pairs(
    i: int,
    j: int,
    heightmap: dict[Coord, int],
) -> list[Coord]:
    point = heightmap[(i, j)]
    indices = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
    return [
        index
        for index in indices
        if index in heightmap and heightmap[index] - point <= 1
    ]


def puzzle1(input_: str) -> int:
    heightmap, start, end = get_heightmap(input_)

    graph = {key: get_adjacent_pairs(*key, heightmap) for key in heightmap}

    dists = bfs(graph, start)
    return dists[end]


def puzzle2(input_: str) -> int:
    heightmap, _, end = get_heightmap(input_)

    graph = {key: get_adjacent_pairs(*key, heightmap) for key in heightmap}

    starts = [k for k, v in heightmap.items() if v == 0]

    all_dists = []
    for start in starts:
        dists = bfs(graph, start)
        if end in dists:
            all_dists.append(dists[end])

    return min(all_dists)


INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
INPUT_X = """\
Sabcabkluv
zzzzzcjmtw
zzzzzdinsx
zzzzzehory
zzzzzfgpqE
"""
EXPECTED_1 = 31
EXPECTED_2 = 29
EXPECTED_1X = 29
EXPECTED_2X = 25


@pytest.mark.parametrize(
    ("input_", "expected", "puzzle"),
    (
        (INPUT, EXPECTED_1, puzzle1),
        (INPUT, EXPECTED_2, puzzle2),
        (INPUT_X, EXPECTED_1X, puzzle1),
        (INPUT_X, EXPECTED_2X, puzzle2),
    ),
)
def test_puzzle(input_, expected, puzzle):
    assert puzzle(input_) == expected


if __name__ == "__main__":
    input_ = read_input()
    print(puzzle1(input_))
    print(puzzle2(input_))
