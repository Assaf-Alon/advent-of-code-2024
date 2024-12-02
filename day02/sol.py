from collections import defaultdict
import math
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def get_parsed_input(input_path: str):
    with open(input_path) as f:
        lines = f.readlines()

        parsed_input = parse_input(lines)
    return parsed_input


def parse_line(line):
    return [int(n) for n in line.split()]


def parse_input(input: List[str]) -> List[List[int]]:
    return [parse_line(line) for line in input]


def get_increasing_sign(n1, n2) -> int:
    return math.copysign(1, n2 - n1)


def get_arr_increasing_sign(arr) -> int:
    """
    If at least 2/3 are increasing (or decreasing),
    the whole sequence should be as well (with the exception of maybe 1)
    """
    if len(arr) < 4:
        return get_increasing_sign(arr[0], arr[1])
    return get_increasing_sign(
        0,
        get_increasing_sign(arr[0], arr[1]) + get_increasing_sign(arr[1], arr[2]) + get_increasing_sign(arr[2], arr[3]),
    )


def get_first_problematic_index(arr, is_increasing) -> Optional[int]:
    for i in range(1, len(arr)):
        diff = arr[i] - arr[i - 1]
        if 1 <= abs(diff) <= 3 and (is_increasing * diff > 0):
            continue
        return i
    return None


def is_error_forgivable(arr, is_increasing, error_index) -> bool:
    levels_without_i = arr.copy()
    levels_without_i.pop(error_index)
    levels_without_i_minus_1 = arr.copy()
    levels_without_i_minus_1.pop(error_index - 1)
    return (
        get_first_problematic_index(levels_without_i, is_increasing) is None
        or get_first_problematic_index(levels_without_i_minus_1, is_increasing) is None
    )


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    parsed_input = get_parsed_input(input_path)
    for levels in parsed_input:
        is_increasing = get_arr_increasing_sign(levels)
        first_problematic_index = get_first_problematic_index(levels, is_increasing)
        sol += int(first_problematic_index is None)

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    parsed_input = get_parsed_input(input_path)
    for levels in parsed_input:
        is_increasing = get_arr_increasing_sign(levels)
        first_problematic_index = get_first_problematic_index(levels, is_increasing)
        if first_problematic_index is None:
            sol += 1
            continue
        sol += int(is_error_forgivable(levels, is_increasing, first_problematic_index))
    handle_solution(sol, expected_output)


def day02():
    solve_part1(EXAMPLE_PATH, 2)
    solve_part1(INPUT_PATH, 287)
    solve_part2(EXAMPLE_PATH, 4)
    solve_part2(INPUT_PATH, 354)


if __name__ == "__main__":
    day02()
