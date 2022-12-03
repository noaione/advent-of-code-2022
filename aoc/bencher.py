# The following module is a module to profile our code using multiple iterations.

import json
import timeit
from pathlib import Path
from typing import Callable, TypedDict

ROOT_DIR = Path(__file__).absolute().parent.parent


class BenchData(TypedDict, total=False):
    part_a: float
    part_b: float


BenchFile = dict[str, BenchData]


def run_with_timeit(func: Callable[[str], str], input_data: str, *, iter: int = 1000) -> float:
    tt = timeit.timeit(lambda: func(input_data), number=1)
    return tt


def read_bench() -> BenchFile:
    bench_file = ROOT_DIR / ".bench"
    if not bench_file.exists():
        return {}
    with bench_file.open() as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def update_bench(day: str, part: str, time: float) -> None:
    bench_file = ROOT_DIR / ".bench"
    data = read_bench()
    if day not in data:
        data[day] = {}
    data[day][part] = time
    with bench_file.open("w") as f:
        json.dump(data, f, indent=4)
