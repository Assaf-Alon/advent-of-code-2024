import math
import os
import re
from typing import List, Optional, Tuple
import numpy as np
from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def parse_input(_input: List[str]):
    A_buttons = []
    B_buttons = []
    targets = []
    for i in range(0, len(_input), 4):
        mtch = re.search(r"Button A: X\+(\d+), Y\+(\d+)", _input[i])
        A_buttons.append((int(mtch.group(1)), int(mtch.group(2))))
        mtch = re.search(r"Button B: X\+(\d+), Y\+(\d+)", _input[i + 1])
        B_buttons.append((int(mtch.group(1)), int(mtch.group(2))))
        mtch = re.search(r"Prize: X=(\d+), Y=(\d+)", _input[i + 2])
        targets.append((int(mtch.group(1)), int(mtch.group(2))))
    return A_buttons, B_buttons, targets


def get_parsed_input(input_path: str):
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def is_linear_dependent(vec1: Tuple[int, int], vec2: Tuple[int, int]) -> bool:
    ratio1 = vec1[0] / vec2[0]
    ratio2 = vec1[1] / vec2[1]
    return math.isclose(ratio1, ratio2, abs_tol=0.001)  # Avoid floating errors


def solve_linear_equations_system(vec1: Tuple[int, int], vec2: Tuple[int, int], target: Tuple[int, int]):
    matrix = [[vec1[0], vec2[0]], [vec1[1], vec2[1]]]
    result = np.linalg.solve(matrix, target)
    return result


def is_mostly_round(num):
    return num % 1 <= 0.0001 or num % 1 >= 0.9999


def is_arr_mostly_round(arr):
    return all([is_mostly_round(n) for n in arr])


def round_to_whole_number_if_close(num):
    if is_mostly_round(num):
        return round(num)
    return num


def round_array(arr):
    return [round_to_whole_number_if_close(n) for n in arr]


def do_vectors_span_result_using_integers(vec1: Tuple[int, int], vec2: Tuple[int, int], target: Tuple[int, int]):
    if is_linear_dependent(vec1, vec2):
        return is_linear_dependent(vec1, target)

    result = solve_linear_equations_system(vec1, vec2, target)
    rounded_results = round_array(result)
    return is_arr_mostly_round(result), rounded_results


def solve_part1(input_path: str, expected_output: Optional[int] = None, is_part2: bool = False):
    A_buttons, B_buttons, targets = get_parsed_input(input_path)
    sol = 0
    for A_button, B_button, target in zip(A_buttons, B_buttons, targets):
        if is_part2:
            target = (target[0] + 10000000000000, target[1] + 10000000000000)
        is_span, result = do_vectors_span_result_using_integers(A_button, B_button, target)
        if not is_span:
            continue
        price = result[0] * 3 + result[1]
        sol += price

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    solve_part1(input_path, expected_output, is_part2=True)


def day13():
    solve_part1(EXAMPLE_PATH, 480)
    solve_part1(INPUT_PATH, 28262)
    solve_part2(EXAMPLE_PATH, 875318608908)
    solve_part2(INPUT_PATH, 101406661266314)


if __name__ == "__main__":
    day13()
