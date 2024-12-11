from collections import defaultdict
import os
import re
from typing import DefaultDict, List, Optional, Set, Tuple

from common import handle_solution, is_in_board, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def parse_input(input_lines: List[str]) -> List[List[int]]:
    return [[int(x) for x in line] for line in input_lines]


def get_parsed_input(input_path: str):
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def count_paths_to_top(
    input_matrix: List[List[int]],
    rows: int,
    cols: int,
    curr_height: int,
    row: int,
    col: int,
    visited_nines: Optional[Set],
):
    if not is_in_board(rows, cols, row, col):
        return 0

    if input_matrix[row][col] != curr_height:
        return 0

    if curr_height == 9:
        if isinstance(visited_nines, set):
            visited_nines.add((row, col))
        return 1

    sol = 0
    for row_diff, col_diff in DIRECTIONS:
        sol += count_paths_to_top(
            input_matrix, rows, cols, curr_height + 1, row + row_diff, col + col_diff, visited_nines
        )
    return sol


def solve(
    input_matrix: List[List[int]], expected_part1: Optional[int] = None, expected_part2: Optional[int] = None
) -> int:
    sol1 = 0
    sol2 = 0
    rows = len(input_matrix)
    cols = len(input_matrix[0])
    for row in range(rows):
        for col in range(cols):
            visited = set()
            paths2 = count_paths_to_top(input_matrix, rows, cols, 0, row, col, visited)
            paths1 = len(visited)
            sol1 += paths1
            sol2 += paths2

    handle_solution(sol1, expected_part1)
    handle_solution(sol2, expected_part2)
    return (sol1, sol2)


def day10():
    solve(get_parsed_input(EXAMPLE_PATH), 36, 81)
    solve(get_parsed_input(INPUT_PATH), 552, 1225)


if __name__ == "__main__":
    day10()
