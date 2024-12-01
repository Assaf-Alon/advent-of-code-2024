from collections import defaultdict
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def parse_input(input: List[str]):
    pass


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    # ...

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    # ...

    handle_solution(sol, expected_output)


def dayXXX():
    solve_part1(EXAMPLE_PATH)
    # solve_part1(INPUT_PATH)
    # solve_part2(EXAMPLE_PATH)
    # solve_part2(INPUT_PATH)


if __name__ == "__main__":
    dayXXX()
