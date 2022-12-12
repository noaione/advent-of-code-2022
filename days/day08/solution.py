import math
from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


def parse(puzzle: str):
    split_trees = [list(map(int, list(puz))) for puz in puzzle.splitlines() if puz]
    edge_row = [0, len(split_trees) - 1]
    edge_col = [0, len(split_trees[0]) - 1]
    return split_trees, edge_row, edge_col


def part_a(puzzle: str) -> str:
    trees, edge_row, edge_col = parse(puzzle)
    # print(ggrid)
    ttemp = len(range(0, edge_row[1] + 1))
    tree_rat = ttemp * 2
    tree_rat += 2 * (ttemp - 2)
    for ridx, tree_row in enumerate(trees):
        if ridx in edge_row:
            continue
        for cidx, ct in enumerate(tree_row):
            if cidx in edge_col:
                continue
            right = trees[ridx][cidx + 1 :]
            left = trees[ridx][:cidx]
            bottom = list(map(lambda x: x[cidx], trees[ridx + 1 :]))
            top = list(map(lambda x: x[cidx], trees[:ridx]))
            comp = (
                ct > max(right),
                ct > max(left),
                ct > max(bottom),
                ct > max(top),
            )
            if any(comp):
                tree_rat += 1
    return str(tree_rat)


def filter_out(movement: list[int], current: int):
    mm = []
    for move in movement:
        mt = move - current
        mm.append(mt)
        if mt >= 0:
            break
    return mm


def part_b(puzzle: str) -> str:
    trees, edge_row, edge_col = parse(puzzle)
    highest = 0
    for ridx, tree_row in enumerate(trees):
        if ridx in edge_row:
            continue
        for cidx, ct in enumerate(tree_row):
            if cidx in edge_col:
                continue
            right = trees[ridx][cidx + 1 :]
            left = trees[ridx][:cidx]
            left.reverse()
            bottom = list(map(lambda x: x[cidx], trees[ridx + 1 :]))
            top = list(map(lambda x: x[cidx], trees[:ridx]))
            top.reverse()
            # print(right, bottom, top, left)

            left = filter_out(left, ct)
            right = filter_out(right, ct)
            bottom = filter_out(bottom, ct)
            top = filter_out(top, ct)
            colt = list(filter(lambda x: x > 0, [len(left), len(right), len(bottom), len(top)]))
            prodt = math.prod(colt)
            if prodt > highest:
                highest = prodt
    return str(highest)


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
