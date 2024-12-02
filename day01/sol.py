from collections import defaultdict
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def parse_input(input: List[str]) -> Tuple[List[int], List[int]]:
    line_pattern = r"^(\d+)\s{3}(\d+)$"
    arr1 = []
    arr2 = []
    for line in input:
        match = re.match(line_pattern, line)
        if not match:
            raise AssertionError("Input is not in the expected format")
        arr1.append(int(match.group(1)))
        arr2.append(int(match.group(2)))
    return arr1, arr2


def get_sorted_arrays(input_path: str) -> Tuple[List[int], List[int]]:
    arr1, arr2 = [], []
    with open(input_path) as f:
        lines = f.readlines()
        arr1, arr2 = parse_input(lines)

    arr1 = sorted(arr1)
    arr2 = sorted(arr2)

    return arr1, arr2


def get_histogram_from_array(array: List[int]) -> DefaultDict:
    hist = defaultdict(lambda: 0)
    for i in array:
        hist[i] += 1

    return hist


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    arr1, arr2 = get_sorted_arrays(input_path)

    for element1, element2 in zip(arr1, arr2):
        sol += abs(element1 - element2)

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    arr1, arr2 = get_sorted_arrays(input_path)
    hist = get_histogram_from_array(arr2)
    for element in arr1:
        sol += hist[element] * element

    handle_solution(sol, expected_output)


def day01():
    solve_part1(EXAMPLE_PATH, 11)
    solve_part1(INPUT_PATH, 1970720)
    solve_part2(EXAMPLE_PATH, 31)
    solve_part2(INPUT_PATH, 17191599)


if __name__ == "__main__":
    day01()
