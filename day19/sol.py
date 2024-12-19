import functools
import os
from typing import List, Optional, Tuple

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def parse_input(_input: List[str]) -> Tuple[Tuple[str], List[str]]:
    available_patterns = _input[0].split(", ")
    desired_patterns = [p for p in _input[2:]]
    return tuple(available_patterns), desired_patterns


def get_parsed_input(input_path: str) -> Tuple[Tuple[str], List[str]]:
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


@functools.lru_cache(maxsize=None)
def count_pattern_possibilities(available_patterns: Tuple[str], desired_pattern: str) -> int:
    if desired_pattern == "":
        return 1

    possibilities = 0
    for p in available_patterns:
        if desired_pattern.startswith(p):
            possibilities += count_pattern_possibilities(
                available_patterns=available_patterns, desired_pattern=desired_pattern[len(p) :]
            )
    return possibilities


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    available, desired = get_parsed_input(input_path)
    sol = 0
    for desired_pattern in desired:
        sol += int(bool(count_pattern_possibilities(available_patterns=available, desired_pattern=desired_pattern)))

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    available, desired = get_parsed_input(input_path)
    sol = 0
    for desired_pattern in desired:
        sol += count_pattern_possibilities(available_patterns=available, desired_pattern=desired_pattern)

    handle_solution(sol, expected_output)


def day19():
    solve_part1(EXAMPLE_PATH, 6)
    solve_part1(INPUT_PATH, 269)
    solve_part2(EXAMPLE_PATH, 16)
    solve_part2(INPUT_PATH, 758839075658876)


if __name__ == "__main__":
    day19()
