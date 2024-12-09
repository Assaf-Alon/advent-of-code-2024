from collections import defaultdict
from itertools import product
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def parse_input(_input: List[str]):
    return _input


def get_parsed_input(input_path: str):
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def is_in_board(rows, cols, row, col):
    return 0 <= row < rows and 0 <= col < cols


def create_hist(input_lines: List[str]):
    hist = defaultdict(lambda: set())
    for row, line in enumerate(input_lines):
        for col, c in enumerate(line):
            if c != ".":
                hist[c].add((row, col))
    return hist


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    lines = get_parsed_input(input_path)
    rows = len(lines)
    cols = len(lines[0])
    hist = create_hist(lines)
    anti_locations = set()
    for c in hist.keys():
        for first, second in product(hist[c], hist[c]):
            if first == second:
                continue
            diff = first[0] - second[0], first[1] - second[1]
            anti_row, anti_col = first[0] + diff[0], first[1] + diff[1]
            if is_in_board(rows, cols, anti_row, anti_col):
                anti_locations.add((anti_row, anti_col))
    sol = len(anti_locations)

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    lines = get_parsed_input(input_path)
    rows = len(lines)
    cols = len(lines[0])
    hist = create_hist(lines)
    anti_locations = set()
    for c in hist.keys():
        for first, second in product(hist[c], hist[c]):
            anti_locations.add(first)
            if first == second:
                continue
            diff = first[0] - second[0], first[1] - second[1]
            anti_row, anti_col = first[0] + diff[0], first[1] + diff[1]
            while is_in_board(rows, cols, anti_row, anti_col):
                anti_locations.add((anti_row, anti_col))
                anti_row, anti_col = anti_row + diff[0], anti_col + diff[1]
    sol = len(anti_locations)
    handle_solution(sol, expected_output)


def day08():
    solve_part1(EXAMPLE_PATH, 14)
    solve_part1(INPUT_PATH, 293)
    solve_part2(EXAMPLE_PATH, 34)
    solve_part2(INPUT_PATH, 934)


if __name__ == "__main__":
    day08()
