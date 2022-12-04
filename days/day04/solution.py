from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


def parse(puzzle: str):
    pairings = [p.split(",") for p in puzzle.splitlines() if p]
    combi = []
    for a, b in pairings:
        aa, ab = a.split("-")
        ba, bb = b.split("-")
        combi.append(
            [
                range(int(aa), int(ab) + 1),
                range(int(ba), int(bb) + 1),
            ]
        )
    return combi


def part_a(puzzle: str) -> str:
    pairs = parse(puzzle)
    # Check if one of the ranges all in the other
    x = 0
    for test_a, test_b in pairs:
        if all([a in test_b for a in test_a]) or all([b in test_a for b in test_b]):
            x += 1
    return str(x)


def part_b(puzzle: str) -> str:
    pairs = parse(puzzle)
    x = 0
    for test_a, test_b in pairs:
        # Check for the one that intersects
        if any([a in test_b for a in test_a]) or any([b in test_a for b in test_b]):
            x += 1
    return str(x)


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
