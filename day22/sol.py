from collections import defaultdict
from math import inf
from operator import xor
import os
from typing import List, Optional


from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
EXAMPLE1_PATH = dir_path + os.sep + "example1.txt"
EXAMPLE2_PATH = dir_path + os.sep + "example2.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

DEBUG = False

def mix(secret: int, result: int) -> int:
    return xor(secret, result)

def prune(secret: int) -> int:
    return secret % 16777216 # pow(2, 24)

def get_parsed_input(input_path: str) -> List[int]:
    lines = read_input_as_lines(input_path)
    return [int(n) for n in lines]

def get_next_pseudurandom(secret: int) -> int:
    step1 = secret * 64 # pow(2, 6)
    secret = prune(mix(secret, step1))

    step2 = secret // 32 # pow(2, 5)
    secret = prune(mix(secret, step2))

    step3 = secret * 2048 # pow(2, 11)
    secret = prune(mix(secret, step3))

    return secret


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    initials = get_parsed_input(input_path)
    for num in initials:
        secret = num
        for _ in range(2000):
            secret = get_next_pseudurandom(secret)
        sol += secret
        
    handle_solution(sol, expected_output)

def get_diff(secret: int, prev: int):
    return (secret % 10) - (prev % 10)

def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    initials = get_parsed_input(input_path)
    profits = defaultdict(lambda: list((0, set())))
    for iter, num in enumerate(initials):
        if DEBUG and iter % 10 == 0:
            print(f"iter = {iter} / {len(initials)}")
        prev = num
        prev4diffs = []
        for _ in range(4):
            secret = get_next_pseudurandom(prev)
            prev4diffs.append(get_diff(secret, prev))
            prev = secret

        for _ in range(4, 2000):
            secret = get_next_pseudurandom(prev)
            prev4diffs.pop(0)
            prev4diffs.append(get_diff(secret, prev))
            diffs = tuple(prev4diffs)
            if num not in profits[diffs][1]:
                profits[diffs][1].add(num)
                profits[diffs][0] += secret % 10
            prev = secret
    
    sol = max([p[0] for p in profits.values()])

    handle_solution(sol, expected_output)


def day22():
    solve_part1(EXAMPLE_PATH, 37327623)
    solve_part1(INPUT_PATH, 15006633487)
    # solve_part2(EXAMPLE1_PATH)
    solve_part2(EXAMPLE2_PATH, 23)
    solve_part2(INPUT_PATH, 1710)


if __name__ == "__main__":
    day22()
