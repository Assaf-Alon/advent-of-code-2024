from collections import defaultdict
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def get_parsed_input(input_path: str) -> Tuple[List[int], List[List[int]]]:
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def parse_input(_input: List[str]) -> Tuple[List[int], List[List[int]]]:
    answers = []
    numbers = []
    for line in _input:
        answer, rest = line.split(":")
        answers.append(int(answer))
        numbers.append([int(num) for num in rest.split(" ") if num != ""])
    return answers, numbers


def get_concat_num(n1: int, n2: int):
    return int(str(n1) + str(n2))


def is_solution_possible(answer: int, numbers: List[int], answer_so_far: int, can_concatenate: bool = False):
    if answer_so_far > answer:
        return False

    if len(numbers) == 0:
        return answer_so_far == answer

    n1 = numbers[0]
    return (
        is_solution_possible(answer, numbers[1:], answer_so_far + n1, can_concatenate)
        or is_solution_possible(answer, numbers[1:], answer_so_far * n1, can_concatenate)
        or (
            can_concatenate
            and is_solution_possible(answer, numbers[1:], get_concat_num(answer_so_far, n1), can_concatenate)
        )
    )


def solve_part1(input_path: str, expected_output: Optional[int] = None, is_part2: bool = False):
    sol = 0
    answers, list_numbers = get_parsed_input(input_path)
    for answer, numbers in zip(answers, list_numbers):
        if is_solution_possible(answer, numbers[1:], numbers[0], is_part2):
            sol += answer

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    solve_part1(input_path, expected_output, True)


def day07():
    solve_part1(EXAMPLE_PATH, 3749)
    solve_part1(INPUT_PATH, 1708857123053)
    solve_part2(EXAMPLE_PATH, 11387)
    solve_part2(INPUT_PATH, 189207836795655)


if __name__ == "__main__":
    day07()
