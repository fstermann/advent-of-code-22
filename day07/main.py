from __future__ import annotations

import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


MAX_SIZE = 100_000

TOTAL_DISK_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000


def puzzle1(input_: str) -> int:
    s: dict[str, dict[str, int]] = {}
    dir_path = []
    dirs = []
    for line in input_.splitlines():
        if line.startswith("$ cd"):
            active_dir = line.split()[2]

            if active_dir != "..":
                dir_path.append(active_dir)
                dir_key = os.path.join(*dir_path)
                s[dir_key] = {}
                dirs.append(dir_key)
            else:
                dir_path.pop()
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            continue
        else:
            size, name = line.split()
            s[os.path.join(*dir_path)][name] = int(size)

    s_sums = {dir_: sum(files.values()) for dir_, files in s.items()}
    total_s = {
        d: sum(size for dir_, size in s_sums.items() if dir_.startswith(d))
        for d in dirs
    }
    return sum(size for size in total_s.values() if size <= MAX_SIZE)


def puzzle2(input_: str) -> int:
    s: dict[str, dict[str, int]] = {}
    dir_path = []
    dirs = []
    for line in input_.splitlines():
        if line.startswith("$ cd"):
            active_dir = line.split()[2]

            if active_dir != "..":
                dir_path.append(active_dir)
                dir_key = os.path.join(*dir_path)
                s[dir_key] = {}
                dirs.append(dir_key)
            else:
                dir_path.pop()
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            continue
        else:
            size, name = line.split()
            s[os.path.join(*dir_path)][name] = int(size)

    s_sums = {dir_: sum(files.values()) for dir_, files in s.items()}
    total_s = {
        d: sum(size for dir_, size in s_sums.items() if dir_.startswith(d))
        for d in dirs
    }

    unused_space = TOTAL_DISK_SPACE - total_s["/"]
    needed_space = REQUIRED_SPACE - unused_space
    return min(size for size in total_s.values() if size >= needed_space)


INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED_1 = 95437
EXPECTED_2 = 24933642


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
