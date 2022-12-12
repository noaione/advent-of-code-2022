from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from importlib import import_module, util
from pathlib import Path
from typing import Callable, Optional

ROOT_DIR = Path(__file__).absolute().parent.parent


@dataclass
class TestCase:
    example: str = ""
    expect: Optional[str] = None
    is_skip: bool = False


@dataclass
class Solution:
    part_a: Optional[Callable[[str], str]] = None
    part_b: Optional[Callable[[str], str]] = None
    parser: Optional[Callable[[str], str]] = None
    puzzle: str = field(repr=False, default="")
    test_a: Optional[TestCase] = None
    test_b: Optional[TestCase] = None

    def __call__(self, puzzle_str: Optional[str] = None):
        # Call both parts if they exist
        self.call_a(puzzle_str=puzzle_str)
        self.call_b(puzzle_str=puzzle_str)

    def call_a(self, puzzle_str: Optional[str] = None, silent: bool = False) -> Optional[str]:
        if self.part_a:
            if not silent:
                print("+ Part A")
            result = self.part_a(puzzle_str or self.puzzle)
            if not silent:
                print(result)
                print()
            return result
        return None

    def call_b(self, puzzle_str: Optional[str] = None, silent: bool = False) -> Optional[str]:
        if self.part_b:
            if not silent:
                print("+ Part B")
            result = self.part_b(puzzle_str or self.puzzle)
            if not silent:
                print(result)
                print()
            return result
        return None

    def test(self, run_a: bool = True, run_b: bool = True) -> tuple[Optional[bool], Optional[bool]]:
        passed: list[Optional[bool]] = [None, None]
        if self.test_a and self.part_a and run_a:
            if not self.test_a.expect:
                print("- Part A: No expected result, skipping")
            elif self.test_a.is_skip:
                print("- Part A: Test ignored, skipping!")
            else:
                res = self.part_a(self.test_a.example)
                if res != self.test_a.expect:
                    print(f"- Part A: Expected {self.test_a.expect}, got {res}")
                    passed[0] = False
                else:
                    print("+ Part A: Test passed")
                    passed[0] = True
        if self.test_b and self.part_b and run_b:
            if not self.test_b.expect:
                print("- Part B: No expected result, skipping")
            elif self.test_b.is_skip:
                print("- Part B: Test ignored, skipping!")
            else:
                res = self.part_b(self.test_b.example)
                if res != self.test_b.expect:
                    print(f"- Part B: Expected {self.test_b.expect}, got {res}")
                    passed[1] = False
                else:
                    print("+ Part B: Test passed")
                    passed[1] = True
        return tuple(passed)


def _find_test_ignore(text: str) -> bool:
    if not text:
        return False
    cleft = text.lstrip()
    if cleft.startswith("# "):
        return "ignore: test" in text.lower()
    if cleft.startswith('"""') or cleft.startswith("'''"):
        return "ignore: test" in text.lower()
    return False


def discover_solution():
    _imported = set()
    DAYS_FOLDER = ROOT_DIR / "days"
    solutions: dict[str, Solution] = {}
    for day in DAYS_FOLDER.iterdir():
        if day.is_dir() and day.name.startswith("day"):
            # Find solution.py inside the file.
            day_solution = day / "solution.py"
            puzzle_data = day / "input.txt"
            if not day_solution.exists():
                continue
            if not puzzle_data.exists():
                continue
            day_dot = "days." + day.name + ".solution"
            if day_dot not in _imported:
                import_module(day_dot)
                _imported.add(day_dot)
            spec = util.spec_from_file_location(day_dot, day_solution)
            if spec is None:
                print(f"Unable to import: {day_solution}")
                continue
            if spec.loader is None:
                print(f"Unable to specify module loader for {day_solution.name}")
                continue
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Find the solution function (part_a, part_b, parta, partb)
            part_a = getattr(module, "part_a", getattr(module, "parta", None))
            part_b = getattr(module, "part_b", getattr(module, "partb", None))
            parser = getattr(module, "parser", getattr(module, "parse", None))
            if part_a is None and part_b is None:
                continue
            solution = Solution()
            if callable(part_a):
                solution.part_a = part_a
            if callable(part_b):
                solution.part_b = part_b
            if callable(parser):
                solution.parser = parser
            examples = day / "example.txt"
            example_data: Optional[str] = None
            if examples.exists():
                example_data = examples.read_text()
            expects = day / "expect.txt"
            expect_data: Optional[str] = None
            header_skip = _find_test_ignore(day_solution.read_text().splitlines()[0])
            if expects.exists():
                expect_data = expects.read_text()
            if example_data and expect_data:
                part_a_expect: Optional[str] = None
                part_b_expect: Optional[str] = None
                for exp in expect_data.strip().splitlines():
                    if exp.startswith("PART A: "):
                        _exp_t = exp[8:].strip()
                        if _exp_t:
                            part_a_expect = _exp_t
                    elif exp.startswith("PART B: "):
                        _exp_t = exp[8:].strip()
                        if _exp_t:
                            part_b_expect = _exp_t
                test_ca = TestCase(example_data, part_a_expect)
                test_cb = TestCase(example_data, part_b_expect)
                skip_a_test = False
                skip_b_test = False
                if part_a is not None:
                    for line in inspect.getsourcelines(part_a):
                        if isinstance(line, int):
                            continue
                        line_s = "".join(line) if isinstance(line, list) else line
                        if _find_test_ignore(line_s):
                            skip_a_test = True
                            break
                if part_b is not None:
                    for line in inspect.getsourcelines(part_b):
                        if isinstance(line, int):
                            continue
                        line_s = "".join(line) if isinstance(line, list) else line
                        if _find_test_ignore(line_s):
                            skip_b_test = True
                            break
                test_ca.is_skip = header_skip or skip_a_test
                test_cb.is_skip = header_skip or skip_b_test
                solution.test_a = test_ca
                solution.test_b = test_cb
            solution.puzzle = puzzle_data.read_text()
            day_parts = int(day.name.replace("day", ""))
            solutions[str(day_parts)] = solution
    # sort by keys
    new_solutions: dict[str, Solution] = {}
    for key in sorted(solutions.keys()):
        new_solutions[key] = solutions[key]
    return new_solutions
