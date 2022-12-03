from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


def get_priority(letter: str) -> int:
    # get as ascii code
    # swap case
    swap = chr(ord(letter) ^ 32)
    minus = 64 if swap.isupper() else 70
    return ord(swap) - minus


def parse_compartments(line: str):
    half = len(line) // 2
    first_part, second_part = line[:half], line[half:]
    return first_part, second_part


def part_a(puzzle: str) -> str:
    pairings = [parse_compartments(puz) for puz in puzzle.splitlines() if puz]
    intersect = [set(a) & set(b) for a, b in pairings]
    sum_data = [sum(get_priority(letter) for letter in intersection) for intersection in intersect]
    return str(sum(sum_data))


def part_b(puzzle: str) -> str:
    puzzlings = [puz for puz in puzzle.splitlines() if puz]
    # group by three pairs
    pairings = [puzzlings[i : i + 3] for i in range(0, len(puzzlings), 3)]
    # get the intersection of each pair
    intersect = [set(puz[0]) & set(puz[1]) & set(puz[2]) for puz in pairings]
    sum_data = [sum(get_priority(letter) for letter in intersection) for intersection in intersect]
    return str(sum(sum_data))


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
