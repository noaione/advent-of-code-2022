from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


def distinct(packet: str, bytes: int = 4):
    for i in range(len(packet)):
        if len(set(packet[i : i + bytes])) == bytes:
            return i + bytes
    raise ValueError("No distinct bytes found")


def part_a(puzzle: str) -> str:
    packet = puzzle.splitlines()[0]
    return str(distinct(packet, 4))


def part_b(puzzle: str) -> str:
    packet = puzzle.splitlines()[0]
    return str(distinct(packet, 14))


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
