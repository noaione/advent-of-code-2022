# ignore: test
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

CURRENT_DIR = Path(__file__).absolute().parent


@dataclass
class Tree:
    name: str
    size: int = 0
    children: list[Tree] = field(default_factory=list)
    parent: Optional[Tree] = field(default=None, repr=False)
    is_file: bool = False


def find_node(nodes: list[Any], dir: str):
    for idx, key in enumerate(nodes):
        if key == dir:
            return idx
        return -1


def make_directory_tree(command_history: str):
    command_histories = [cmd for cmd in command_history.splitlines() if cmd]
    directory_tree = Tree(name="/")
    start_aggregate = False
    current_tree = directory_tree
    for cmd in command_histories:
        split_space = cmd.rsplit(" ", 1)
        if cmd.startswith("$ cd"):
            if ".." in split_space[1]:
                if current_tree.parent is None:
                    raise ValueError("Cannot move up from root directory")
                # Move back a directory
                current_tree = current_tree.parent
            elif split_space[1] == "/":
                current_tree = directory_tree
            else:
                if current_tree.is_file:
                    raise ValueError("Cannot change directory into a file")
                current_dir = split_space[1]
                # Find node in tree
                tree_change = False
                for idx, key in enumerate(current_tree.children):
                    if key.name == current_dir:
                        current_tree = current_tree.children[idx]
                        tree_change = True
                        break
                if not tree_change:
                    # Add new tree node
                    current_tree.children.append(Tree(name=current_dir, parent=current_tree))
                    current_tree = current_tree.children[-1]
            continue
        if cmd.startswith("$ ls"):
            start_aggregate = True
            continue
        if cmd.startswith("$ ") and start_aggregate:
            start_aggregate = False
            continue
        if start_aggregate:
            size, name = cmd.split(" ", 1)
            if size == "dir":
                # Add new tree node
                current_tree.children.append(Tree(name=name, parent=current_tree))
            else:
                size_i = int(size)
                # Add to current tree size
                current_tree.children.append(Tree(name=name, size=size_i, parent=current_tree, is_file=True))

    # Now aggregate the sizes for the directory tree
    # Aggregate from the bottom up
    return directory_tree


def print_tree(tree: Tree, level: int = 0):
    print(f"{'  ' * level}- {tree.name} ({tree.size})")
    for child in tree.children:
        print_tree(child, level + 1)


def sum_tree_size(tree: Tree, max_size: int, aggregate_total: int = 0):
    if tree.is_file:
        return tree.size

    current_total = aggregate_total
    temp_total = 0
    to_be_tested: list[Tree] = []
    for child in tree.children:
        if child.is_file:
            temp_total += child.size
        else:
            to_be_tested.append(child)
    if temp_total <= max_size:
        current_total += temp_total
    if len(to_be_tested) > 0:
        temp_child_total = []
        for child in to_be_tested:
            print(child.name)
            temp_child_total.append(sum_tree_size(child, max_size, current_total))
        sum_all = sum(temp_child_total)
        temp_diff = sum_all - temp_total
        new_total = temp_total + temp_diff
        if new_total <= max_size:
            current_total += new_total
    print(f"Current total: {current_total}")
    return current_total


def part_a(puzzle: str) -> str:
    dir_tree = make_directory_tree(puzzle)
    print_tree(dir_tree)
    print(sum_tree_size(dir_tree, 100000))
    # Find directory (except root) with the size at most 100000
    return "Not implemented"


def part_b(puzzle: str) -> str:
    return "Not implemented"


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
