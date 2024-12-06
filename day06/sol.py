from collections import defaultdict
import os
from typing import List, Optional, Tuple

from common import handle_solution, read_input_as_matrix

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

INITIAL_DIRECTION = (-1, 0)


def get_guard_location(input: List[List[str]]):
    for i, line in enumerate(input):
        try:
            guard_col = line.index("^")
        except:
            continue
        print(f"Guard location: {i, guard_col}")
        return (i, guard_col)
    raise ValueError("Guard not found")


def get_next_direction(curr_direction: Tuple[int, int]):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    index = directions.index(curr_direction)
    next_index = (index + 1) % 4
    return directions[next_index]


def is_about_to_hit_obstacle(board: List[str], curr_location: Tuple[int, int], curr_direction: Tuple[int, int]):
    curr_x, curr_y = curr_location
    dir_x, dir_y = curr_direction
    return board[curr_x + dir_x][curr_y + dir_y] == "#"


def is_legal_step(board: List[str], curr_location: Tuple[int, int], curr_direction: Tuple[int, int]):
    rows = len(board)
    cols = len(board[0])
    next_row = curr_location[0] + curr_direction[0]
    next_col = curr_location[1] + curr_direction[1]
    return 0 <= next_row < rows and 0 <= next_col < cols


def print_board(board: List[List[str]], direction: Tuple[int, int]):
    for line in board:
        print(line)
    print(f"direction: {direction}")
    print("-----" * len(board[0]))


def move_guard(board: List[str], curr_location: Tuple[int, int], curr_direction: Tuple[int, int]):
    while is_about_to_hit_obstacle(board, curr_location, curr_direction):
        curr_direction = get_next_direction(curr_direction)
    row, col = curr_location
    row_dir, col_dir = curr_direction
    new_position = board[row][col] != "X"
    board[row][col] = "X"

    return (row + row_dir, col + col_dir), curr_direction, new_position


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    board = read_input_as_matrix(input_path)
    (row, col) = get_guard_location(board)
    direction = INITIAL_DIRECTION
    visited_locations = set()
    visited_locations.add((row, col))
    while is_legal_step(board, (row, col), direction):
        (row, col), direction, new_position = move_guard(board, (row, col), direction)
        sol += int(new_position)
        visited_locations.add((row, col))

    sol += board[row][col] != "X"
    handle_solution(sol, expected_output)
    return visited_locations


def is_looped(board: List[List[str]], initial_position: Tuple[int, int], initial_direction: Tuple[int, int]):
    row, col = initial_position
    hist = defaultdict(lambda: 0)
    direction = initial_direction
    while is_legal_step(board, (row, col), direction):
        (row, col), direction, new_position = move_guard(board, (row, col), direction)
        hist[(row, col)] += 1
        if hist[(row, col)] > 4:
            return True
    return False


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    board = read_input_as_matrix(input_path)
    initial_position = get_guard_location(board)
    visited_locations = solve_part1(input_path)
    for i, position in enumerate(visited_locations):
        if i % 100 == 0:
            print(f"{i} / {len(visited_locations)}")
        if position == initial_position:
            continue
        row, col = position
        prev_value = board[row][col]
        board[row][col] = "#"
        sol += int(is_looped(board, initial_position, INITIAL_DIRECTION))
        board[row][col] = prev_value

    handle_solution(sol, expected_output)


def day06():
    solve_part1(EXAMPLE_PATH, 41)
    solve_part1(INPUT_PATH, 5312)
    solve_part2(EXAMPLE_PATH, 6)
    solve_part2(INPUT_PATH, 1748)


if __name__ == "__main__":
    day06()
