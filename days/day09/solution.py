# ignore: test
import pprint
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CURRENT_DIR = Path(__file__).absolute().parent


@dataclass
class Move:
    direction: Literal["U", "D", "L", "R"]
    amount: int

    @classmethod
    def from_puzzle(cls, data: str):
        direct, amount = data.split(" ", 1)
        return cls(direct.upper(), int(amount))  # type: ignore


def parse(puzzle: str) -> list[Move]:
    return [Move.from_puzzle(puz) for puz in puzzle.splitlines() if puz]


def make_grid(movements: list[Move]):
    """
    Create the grid from the movements which will be populated
    later.

    Start from 0,0 and move in the direction of the movement
    with the amount, extend the grids as needed.

    0,0 is located on bottom-left, if the movement go on the
    minus side, stop extending the grid and just ignore the
    rest of the movement.

    Do not raise error if the movement is invalid, just ignore
    """
    # fmt: off
    # [
    #   [column], # row
    #   [column], # row
    #   [column], # row
    # ]
    grids = [
        # (0, 0)
        [0],
    ]
    # fmt: on
    # x, y
    current_pos = (0, 0)
    for move in movements:
        if move.direction == "U":
            current_pos = (current_pos[0], current_pos[1] - move.amount)
            if current_pos[1] < len(grids):
                for _ in range(move.amount):
                    grids.insert(0, [0] * len(grids[0]))
        elif move.direction == "R":
            current_pos = (current_pos[0] + move.amount, current_pos[1])
            if current_pos[0] > len(grids[current_pos[1]]):
                grids[current_pos[1]].extend([0] * (current_pos[0] - len(grids[current_pos[1]])))
        elif move.direction == "L":
            current_pos = (current_pos[0] - move.amount, current_pos[1])
            if current_pos[0] < 0:
                current_pos = (0, current_pos[1])  # limit to x=0
        elif move.direction == "D":
            current_pos = (current_pos[0], current_pos[1] + move.amount)
            # Max y is len(grids) - 1
            if current_pos[1] > len(grids) - 1:
                # STOP down movement
                current_pos = (current_pos[0], len(grids) - 1)
        else:
            raise ValueError("Invalid direction")

    # Find longest row, then copy it to all rows
    for row in grids.copy():
        if len(row) > len(grids[0]):
            grids[0] = row[:]
    grids[0].append(0)
    for idx, row in enumerate(grids[1:].copy(), 1):
        grids[idx] = grids[0][:]
    # grids[0].append(0)
    return grids


def part_a(puzzle: str) -> str:
    parsed_move = parse(puzzle)
    grids_data = make_grid(parsed_move)
    # In part A, we will do a simple planck rope simulation
    # We have a (H)ead and (T)ail of a rope with the max
    # stress of 1 pixel.
    # For example:
    # [. . .]
    # [. . .]
    # [s . .]  # T and H are at (s)tart position
    # Move right by 2:
    # [. . .]
    # [. . .]
    # [s T H]
    # Move top by 1:
    # [. . .]
    # [. . H]
    # [s T .]
    # Move top by 1:
    # [. . H]
    # [. . T]
    # [s . .]
    # Move right by 1:
    # [. . H]  # T and H are at the same position
    # [. . .]
    # [s . .]

    # Start from bottom-left
    max_y = len(grids_data) - 1
    max_x = len(grids_data[0]) - 1
    current_pos_H: list[int] = [0, max_y]
    current_pos_T: list[int] = [0, max_y]
    grids_data[max_y][0] = 1
    print(max_x, max_y)
    for move in parsed_move:
        STOP_MOVE = False
        for step in range(move.amount):
            if STOP_MOVE:  # it's useless to move, just break to make it faster
                break
            if move.direction == "U":
                current_pos_H[1] -= 1
                current_pos_T[1] -= 0 if step == 0 else 1
                try:
                    grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                except IndexError:
                    # Let's ignore!
                    pass
                # Check if H and T are on different x-axis
                # ex:
                # [. . .]
                # [. T H]
                # We want to move H up by one
                # Ignore the T
                # Then on the second step, we want to move H up by one
                # Move the T to the same x-axis as H
                # Then move it up by one
                if current_pos_H[0] != current_pos_T[0] and move.amount > 1:
                    current_pos_T[0] = current_pos_H[0]
                    # We don't want to count this as visited.
                if current_pos_H[1] < 0:
                    current_pos_H[1] = 0
                    # Check if there's more step to move
                    # If yes, just ignore the rest of the step
                    # Set both H and T to the same position
                    if step < move.amount - 1:
                        current_pos_T[1] = current_pos_H[1]
                        grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                        STOP_MOVE = True
            elif move.direction == "R":
                # Do the same thing as U except the x-axis
                current_pos_H[0] += 1
                current_pos_T[0] += 0 if step == 0 else 1
                try:
                    grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                except IndexError:
                    # Let's ignore!
                    pass
                print("R", current_pos_H, current_pos_T)
                pprint.pprint(grids_data)
                # ROPE CHECK, If it's on different y-axis,
                # [. T . .]
                # [. H . .]
                # Do not move T when H move by 1
                # [. T . .]
                # [. . H .]
                # Still do not move T
                # [. T . .]
                # [. . . H]
                # Move T to the same y-axis as H and move it by 1
                if current_pos_H[0] > max_x:
                    current_pos_H[0] = max_x
                    if step < move.amount - 1:
                        current_pos_T[0] = current_pos_H[0]
                        grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                        STOP_MOVE = True
            elif move.direction == "D":
                # Do the same thing as U except the y-axis
                current_pos_H[1] += 1
                current_pos_T[1] += 0 if step == 0 else 1
                try:
                    grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                except IndexError:
                    pass
                if current_pos_H[0] != current_pos_T[0] and move.amount > 1:
                    current_pos_T[0] = current_pos_H[0]
                if current_pos_H[1] > max_y:
                    current_pos_H[1] = max_y
                    if step < move.amount - 1:
                        current_pos_T[1] = current_pos_H[1]
                        grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                        STOP_MOVE = True
            elif move.direction == "L":
                # Do the same thing as U except the x-axis
                current_pos_H[0] -= 1
                current_pos_T[0] -= 0 if step == 0 else 1
                try:
                    grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                except IndexError:
                    pass
                if current_pos_H[1] != current_pos_T[1] and move.amount > 1:
                    current_pos_T[1] = current_pos_H[1]
                if current_pos_H[0] < 0:
                    current_pos_H[0] = 0
                    if step < move.amount - 1:
                        current_pos_T[0] = current_pos_H[0]
                        grids_data[current_pos_T[1]][current_pos_T[0]] = 1
                        STOP_MOVE = True
        print(current_pos_H, current_pos_T, "||", move.direction, move.amount)
        pprint.pprint(grids_data)
    # count all the visited grids
    return str(sum(sum(row) for row in grids_data))


def part_b(puzzle: str) -> str:
    return "Not implemented"


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
