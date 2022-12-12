from dataclasses import dataclass
from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


@dataclass
class Cycle:
    x: int

    @classmethod
    def from_puzzle(cls, line: str):
        if line.startswith("noop"):
            return cls(0)
        # addx
        return Cycle(int(line.split(" ", 1)[1]))


def parse(puzzle: str):
    cycles = [Cycle.from_puzzle(line) for line in puzzle.splitlines() if line]
    return cycles


def sum_cycles(cycles: list[Cycle], max_cycle: int):
    current = 1
    total = 1
    for cycle in cycles:
        # only one cycle (noop)
        if cycle.x == 0:
            current += 1
            continue
        # addx takes 2 cycles
        for _ in range(2):
            current += 1
        if current > max_cycle:
            return total
        total += cycle.x
    return -1


def part_a(puzzle: str) -> str:
    cycles = parse(puzzle)
    cycle_20 = sum_cycles(cycles, 20)
    cycle_60 = sum_cycles(cycles, 60)
    cycle_100 = sum_cycles(cycles, 100)
    cycle_140 = sum_cycles(cycles, 140)
    cycle_180 = sum_cycles(cycles, 180)
    cycle_220 = sum_cycles(cycles, 220)
    return str(
        (cycle_20 * 20)
        + (cycle_60 * 60)
        + (cycle_100 * 100)
        + (cycle_140 * 140)
        + (cycle_180 * 180)
        + (cycle_220 * 220)
    )


def part_b(puzzle: str) -> str:
    # ignore: test
    drawings = []
    cycles = parse(puzzle)
    for cycle_row in [20]:
        current = 1
        total = 1
        current_draw = ""
        for cycle in cycles:
            # only one cycle (noop)
            if cycle.x == 0:
                current += 1
                continue
            # addx takes 2 cycles
            for _ in range(2):
                current += 1
                middle_pix = total - current
                if middle_pix in [-1, 0, 1]:
                    current_draw += "#"
                else:
                    current_draw += "."
            total += cycle.x
        print(f"{cycle_row}: {total}")
        drawings.append(current_draw)
    print("\n".join(drawings))
    return "Not implemented"


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
