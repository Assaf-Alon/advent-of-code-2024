import os
from pprint import pprint
from typing import List, Optional


from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

MAX_HEIGHT = 5

DEBUG = True


def get_hist(lines: List[str]):
    hist = [[lines[i][j] for i in range(len(lines))].count("#") - 1 for j in range(len(lines[0]))]
    return hist


def parse_current_lockey(lines: List[str], curr_line_index: int, locks: List[List[int]], keys: List[List[int]]):
    start_index = curr_line_index
    while curr_line_index < len(lines) and lines[curr_line_index] != "":
        curr_line_index += 1

    end_index = curr_line_index
    curr_line_index += 1
    hist = get_hist(lines[start_index:end_index])

    line = lines[start_index]
    if all([c == "#" for c in line]):
        locks.append(hist)
    else:
        assert all([c == "." for c in line])
        keys.append(hist)

    return curr_line_index


def does_key_fit_lock(key: List[int], lock: List[int]) -> bool:
    return all(key[i] + lock[i] <= MAX_HEIGHT for i in range(len(key)))


def parse_input(input_path: str):
    lines = read_input_as_lines(input_path)
    keys = []
    locks = []
    curr_line_index = 0
    while curr_line_index < len(lines):
        curr_line_index = parse_current_lockey(lines, curr_line_index, locks, keys)

    return locks, keys


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    locks, keys = parse_input(input_path)
    if DEBUG:
        pprint(locks)
        print("---------------")
        pprint(keys)

    for key in keys:
        for lock in locks:
            sol += int(does_key_fit_lock(key, lock))
    return handle_solution(sol, expected_output)


def day25():
    # solve_part1(EXAMPLE_PATH, 3)
    solve_part1(INPUT_PATH, 3133)


if __name__ == "__main__":
    day25()
