from dataclasses import dataclass, field
from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


@dataclass
class Stack:
    boxs: list[str] = field(default_factory=list)

    def get_top(self):
        return self.boxs[-1]

    def add(self, box: str):
        self.boxs.append(box)

    def push_back(self, box: str):
        self.boxs.insert(0, box)

    def remove(self):
        return self.boxs.pop()


@dataclass
class Move:
    amount: int
    to: str
    fr: str


def parse(cranes_data: str):
    stacks, movements = cranes_data.split("\n\n", 1)
    stacks_row = stacks.split("\n")
    row_num = stacks_row.pop()
    stacks_box = {num.strip(): Stack() for num in row_num.lstrip().split(" ") if num}
    for st_row in stacks_row:
        st_row = st_row
        pos = 1
        for idx, row in enumerate(st_row, 1):
            # [H]                 [Z]         [J]
            if idx % 4 == 0:
                continue
            if idx % 2 == 0:
                # Every other space
                if row.strip():
                    stacks_box[str(pos)].push_back(row)
                pos += 1
    move_temp = [m.split(" ") for m in movements.split("\n") if m]
    move_parse = [Move(amount=int(m[1]), fr=m[3], to=m[5]) for m in move_temp]
    return stacks_box, move_parse


def part_a(puzzle: str) -> str:
    stacks, moves = parse(puzzle)
    for move in moves:
        for _ in range(move.amount):
            try:
                pop = stacks[move.fr].remove()
                stacks[move.to].add(pop)
            except IndexError:
                pass
    return "".join([stack.get_top() for stack in stacks.values()])


def part_b(puzzle: str) -> str:
    stacks, moves = parse(puzzle)
    for move in moves:
        ordering = []
        for _ in range(move.amount):
            try:
                pop = stacks[move.fr].remove()
                ordering.insert(0, pop)
            except IndexError:
                pass
        stacks[move.to].boxs.extend(ordering)
    return "".join([stack.get_top() for stack in stacks.values()])


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
