import os
from pathlib import Path
from textwrap import dedent
from typing import Optional

import click
import requests
from dotenv import load_dotenv

from .discover import discover_solution

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
ROOT_DIR = Path(__file__).absolute().parent.parent
dotenv_file = ROOT_DIR / ".env"
if dotenv_file.exists():
    load_dotenv(dotenv_file)

PREPARE_TEXT = """from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent


def part_a(puzzle: str) -> str:
    return "Not implemented"


def part_b(puzzle: str) -> str:
    return "Not implemented"


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
"""


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(
    "0.1.0",
    "--version",
    "-V",
    prog_name="aoc",
    message="%(prog)s v%(version)s - Created by noaione",
)
@click.pass_context
def main(ctx: click.Context):
    """
    A CLI tool to run Advent of Code solutions.
    """
    pass


@main.command(
    name="run",
    help="Run specific day's solution",
)
@click.argument("day", type=str, required=False)
def run_function(day: Optional[str] = None):
    """
    Run a specific day's solution.
    """
    # Discover the solution
    solution = discover_solution()
    if not day:
        print("++ Available solutions:")
        if not solution:
            print("No solutions found.")
            return 0
        for day_str, sol in solution.items():
            day_i = int(day_str)
            print(f"- {day_i:02d}", end="")
            if sol.part_a:
                print(".a", end="")
            if sol.part_b:
                print(f", {day_i:02d}.b", end="")
            print()
        print("\nJust do: `aoc run 01` to run all solutions for day 1.")
        print("Or: `aoc run 01.a` to run only part a for day 1 as an example.")
        return 0

    split_data = day.split(".", 1)
    if len(split_data) == 2:
        day_sel, part_sel = split_data
        if part_sel.lower() not in ["a", "b"]:
            print("Invalid part selected.")
            return 1

        try:
            day_ii = int(day_sel)
        except ValueError:
            print("Invalid day selected (must be an integer).")
            return 1
    else:
        try:
            day_ii = int(split_data[0])
        except ValueError:
            print("Invalid day selected (must be an integer).")
            return 1

        part_sel = None
    if str(day_ii) not in solution:
        print("Day not found.")
        return 1

    sel_sol = solution[str(day_ii)]
    if part_sel is None:
        sel_sol()
    elif part_sel == "a":
        sel_sol.call_a()
    elif part_sel == "b":
        sel_sol.call_b()


@main.command(
    name="test",
    help="Test specific day's solution",
)
@click.argument("day", type=str, required=False)
def test_function(day: Optional[str] = None):
    """
    Test a specific day's solution.
    """
    # Discover the solution
    solution = discover_solution()
    if not day:
        print("++ Available solutions:")
        if not solution:
            print("No solutions found.")
            return 0
        for day_str, sol in solution.items():
            day_i = int(day_str)
            print(f"- {day_i:02d}", end="")
            if sol.part_a:
                print(".a", end="")
            if sol.part_b:
                print(f", {day_i:02d}.b", end="")
            print()
        print("\nJust do: `aoc test 01` to test all solutions for day 1.")
        print("Or: `aoc test 01.a` to test only part a for day 1 as an example.")
        return 0

    split_data = day.split(".", 1)
    if len(split_data) == 2:
        day_sel, part_sel = split_data
        if part_sel.lower() not in ["a", "b"]:
            print("Invalid part selected.")
            return 1

        try:
            day_ii = int(day_sel)
        except ValueError:
            print("Invalid day selected (must be an integer).")
            return 1
    else:
        try:
            day_ii = int(split_data[0])
        except ValueError:
            print("Invalid day selected (must be an integer).")
            return 1

        part_sel = None
    if str(day_ii) not in solution:
        print("Day not found.")
        return 1

    sel_sol = solution[str(day_ii)]
    if part_sel is None:
        sel_sol.test()
    elif part_sel == "a":
        sel_sol.test(run_b=False)
    elif part_sel == "b":
        sel_sol.test(run_a=False)


@main.command(
    name="prepare",
    help="Prepare a new day's solution",
)
@click.argument("day", type=int)
@click.option("-y", "--year", type=int, default=2022, help="Year to prepare for")
@click.option("-f", "--force", is_flag=True, help="Force overwrite puzzle files")
def prepare_function(day: int, year: int, force: bool):
    """
    Prepare a new day's solution.
    """
    session_env = os.environ.get("AOC_SESSION")
    if session_env is None:
        print("AOC_SESSION environment variable is not set.")
        return 1

    print(f"+ Preparing day {day}...")
    days_folder = ROOT_DIR / "days" / f"day{day:02d}"
    if days_folder.exists() and not force:
        print(f"Day {day} already exists. Use --force to overwrite.")
        return 1

    days_folder.mkdir(parents=True, exist_ok=True)
    solution_file = days_folder / "solution.py"
    if not solution_file.exists():
        solution_file.write_text(PREPARE_TEXT)

    print(f"+ Downloading puzzle data for day {day}...")
    r = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": session_env})
    puzzle_file = days_folder / "input.txt"
    r.raise_for_status()
    puzzle_file.write_text(r.text)
    print(f"Day {day} prepared successfully.")
