from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


def common(puzzle: str):
    split_doubles = puzzle.split("\n\n")
    all_numbers = [sum([int(number) for number in group.split("\n") if number]) for group in split_doubles]
    return all_numbers


def part_a(puzzle: str) -> str:
    all_numbers = common(puzzle)
    return str(max(all_numbers))


def part_b(puzzle: str):
    all_numbers = sorted(common(puzzle), reverse=True)
    return str(sum(all_numbers[:3]))


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
