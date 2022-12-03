# The following module is a module to profile our code using multiple iterations.

import timeit
from typing import Callable


def run_with_timeit(func: Callable[[str], str], input_data: str, *, iter: int = 1000) -> float:
    tt = timeit.timeit(lambda: func(input_data), number=1)
    return tt
