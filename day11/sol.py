import os
from typing import Dict, List, Optional

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def should_cache(n: int) -> bool:
    # return len(str(n)) < 30
    return True


def transform_number_x_times(num: int, times: int, cache: Dict) -> int:
    c = cache.get((num, times))
    if c:
        return c

    if times == 1:
        t = transform_number(num)
        if should_cache(num):
            cache[(num, 1)] = len(t)
        return len(t)

    t = transform_number(num)
    out = 0
    for n in t:
        t2 = transform_number_x_times(n, times - 1, cache)
        out += t2
    if should_cache(num):
        cache[(num, times)] = out
    return out


def transform_number(num: int) -> List[int]:
    if num == 0:
        return [1]

    s = str(num)
    l = len(s)
    if l % 2 == 0:
        return [int(s[: (l // 2)]), int(s[(l // 2) :])]

    return [num * 2024]


def parse_input(_input: List[str]):
    return [int(n) for n in _input[0].split(" ")]


def get_parsed_input(input_path: str):
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def solve(input_path: str, expected_output: Optional[int] = None, blinks: int = 25):
    sol = 0
    cache = dict()
    nums = get_parsed_input(input_path)
    for num in nums:
        transformed = transform_number_x_times(num, blinks, cache)
        sol += transformed

    handle_solution(sol, expected_output)


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    solve(input_path, expected_output, 25)


def solve_part2(input_path: str, expected_output: Optional[int] = None, blinks=75):
    solve(input_path, expected_output, 75)


def day11():
    solve_part1(EXAMPLE_PATH, 55312)
    solve_part1(INPUT_PATH, 217812)
    solve_part2(EXAMPLE_PATH, 65601038650482)
    solve_part2(INPUT_PATH, 259112729857522)


if __name__ == "__main__":
    day11()
