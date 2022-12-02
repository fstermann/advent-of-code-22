def read_input() -> str:
    with open("day01/input.txt", "r") as f:
        return f.read()


def puzzle1(input_: str) -> int:
    elves_calories = input_.split(sep="\n\n")
    return max(sum(int(cal) for cal in cals.split("\n")) for cals in elves_calories)


def puzzle2(input_: str) -> int:
    elves_calories = input_.split(sep="\n\n")
    return sum(
        sorted(sum(int(cal) for cal in cals.split("\n")) for cals in elves_calories)[
            -3:
        ]
    )


if __name__ == "__main__":
    input_ = read_input()
    print(puzzle1(input_))
    print(puzzle2(input_))
