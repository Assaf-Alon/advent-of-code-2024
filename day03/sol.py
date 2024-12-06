from collections import defaultdict
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution, read_input_as_string

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

MUL_REGEX_PATTERN = r"^mul\((\d{1,3}),(\d{1,3})\)"
DO_PATTERN = "^do\(\)"
DONT_PATTERN = "^don't\(\)"

ENABLE = "e"
DISABLE = "d"
NO_MATCH = "n"


def try_matching_mul_command(input, position):
    assert input[position] == "m"
    relevant_slice = input[position : position + 12]
    match_or_none = re.match(MUL_REGEX_PATTERN, relevant_slice)
    if match_or_none is None:
        # <mul outcome>, <pos addition>
        return 0, 1
    outcome = int(match_or_none.group(1)) * int(match_or_none.group(2))
    pos_addition = match_or_none.span()[1]
    return outcome, pos_addition


def try_matching_toggling_command(input, position):
    assert input[position] == "d"
    relevant_slice = input[position : position + 8]
    match_outcome = re.match(DO_PATTERN, relevant_slice)
    if match_outcome is not None:
        return ENABLE, 4

    match_outcome = re.match(DONT_PATTERN, relevant_slice)
    if match_outcome is not None:
        return DISABLE, 7

    return NO_MATCH, 1


def parse_input(input: List[str]):
    pass


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    position = 0
    input_string = read_input_as_string(input_path)
    while position < len(input_string):
        if input_string[position] != "m":
            position += 1
            continue

        outcome, pos_addition = try_matching_mul_command(input_string, position)
        sol += outcome
        position += pos_addition

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    position = 0
    toggle = ENABLE
    input_string = read_input_as_string(input_path)
    while position < len(input_string):
        pos_addition = 1
        sol_addition = 0
        if input_string[position] == "m" and toggle == ENABLE:
            sol_addition, pos_addition = try_matching_mul_command(input_string, position)

        if input_string[position] == "d":
            output, pos_addition = try_matching_toggling_command(input_string, position)
            if output != NO_MATCH:
                toggle = output

        sol += sol_addition
        position += pos_addition

    handle_solution(sol, expected_output)


def day03():
    solve_part1(EXAMPLE_PATH, 161)
    solve_part1(INPUT_PATH, 184122457)
    solve_part2(EXAMPLE_PATH, 48)
    solve_part2(INPUT_PATH, 107862689)


if __name__ == "__main__":
    day03()
