from collections import defaultdict
import os
from typing import List, Optional, Tuple

from common import handle_solution, read_input_as_matrix

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

WORD_TO_SEARCH = "XMAS"
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def check_bounds(row, col, row_count, col_count):
    result = 0 <= row < row_count and 0 <= col < col_count
    return result


def check_bounds_for_x_middle(row, col, row_count, col_count):
    return check_bounds(row - 1, col - 1, row_count - 2, col_count - 2)


def count_words_from_cell(matrix, row, col, row_count, col_count, word_index=0, direction=None):
    if word_index == len(WORD_TO_SEARCH):
        prev_row = row - direction[0]
        prev_col = col - direction[1]
        return 1

    if not check_bounds(row, col, row_count, col_count):
        return 0

    if matrix[row][col] != WORD_TO_SEARCH[word_index]:
        return 0

    # Already heading torwards some direction, don't branch out
    if direction is not None:
        row_diff, col_diff = direction
        new_row = row + row_diff
        new_col = col + col_diff
        return count_words_from_cell(matrix, new_row, new_col, row_count, col_count, word_index + 1, direction)

    # Search in all direction
    cnt = 0
    for row_diff, col_diff in DIRECTIONS:
        new_row = row + row_diff
        new_col = col + col_diff
        if not check_bounds(new_row, new_col, row_count, col_count):
            continue
        cnt += count_words_from_cell(
            matrix,
            new_row,
            new_col,
            row_count,
            col_count,
            word_index + 1,
            (row_diff, col_diff),
        )
    return cnt


def count_x_from_cell(matrix, row, col, row_count, col_count, word_index=0, direction=None):
    if not check_bounds_for_x_middle(row, col, row_count, col_count):
        return 0

    if matrix[row][col] != "A":
        return 0

    top_left = matrix[row - 1][col - 1]
    top_right = matrix[row - 1][col + 1]
    bottom_left = matrix[row + 1][col - 1]
    bottom_right = matrix[row + 1][col + 1]
    chars = (top_left, top_right, bottom_left, bottom_right)
    count_chars = defaultdict(lambda: 0)
    for c in chars:
        count_chars[c] += 1

    if count_chars["S"] != 2 or count_chars["M"] != 2:
        return 0

    if top_left == bottom_right:
        return 0

    return 1


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    total_count = 0
    matrix = read_input_as_matrix(input_path)
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            total_count += count_words_from_cell(
                matrix,
                row_index,
                col_index,
                len(matrix),
                len(row),
            )
    handle_solution(total_count, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    total_count = 0
    matrix = read_input_as_matrix(input_path)
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            total_count += count_x_from_cell(
                matrix,
                row_index,
                col_index,
                len(matrix),
                len(row),
            )
    handle_solution(total_count, expected_output)


def day04():
    solve_part1(EXAMPLE_PATH, 18)
    solve_part1(INPUT_PATH, 2447)
    solve_part2(EXAMPLE_PATH, 9)
    solve_part2(INPUT_PATH, 1868)


if __name__ == "__main__":
    day04()
