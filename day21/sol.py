# =======================
# DISCLAIMER
# ----------
# This was a tough one, I wasn't too far off, but haven't managed to figure out how to
# elegantly decide the better order, which is to give priority to:
# [1] Repeating moves (quite easy)
# [2] Leftmost steps (<) before middle (^, v) before rightmost (>) (didn't understand why)
# Reference used:
# https://topaz.github.io/paste/#XQAAAQBIAwAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q16fMXrmVEJ7Evm5vduWQrd/+QN/sT5NTFllVFTjgKJP6OxgrBHlhvPS7A6wbJIoMWrNe2tyT97qwYTRCsgVQfBx823LTTY
# /1Kxpf4sn4VlsNif99Axe8QN6AuRiCMsruHP45JPOrmEaM
# +ugUDAtkP6mPCrsYtDrJateAX7f6jFjlg2NGmUpxHuceHKy6Rsk2XczBKmmW9aX11JgQKPad
# /Lsb2Tvm2GFxxI4jorxvgQFg3TZSUrE04sXFCRvadQytzwVZrseGkNL5tob0xmcezEud3o9V3QoDefBM7KItck1je16SdyZznPWSL
# +WC2CojR2IXSU52yWr6paKb4S2dco3u1f6MndYi0P7cZTrJeZEwfwOsuNx9yfXm8N+x0Jw
# /GN5npCjMfCeZeyrpArhE6UvApVTAsNN6IS4pIKB9CA0SKtMgvzfZv09013o7nSyeqG73t1loRnUUdvp50fWxyTX5
# +Tt1kMdCO92X9CdCtss3bEDilwaa0wsPFWrjb8OWzoXDPsB2
# +mFp+lBddO6UK9BXoBIrvOlog+GNFBFgB49+lG3yf
# //g3jtj39eW6iGLK8v6Htc+YP/wkL3AA=
# =================================================================


from collections import Counter
import os
from typing import Dict, Optional, Tuple

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

DEBUG = False

NUMPAD_POSITIONS = {c: (i // 3, i % 3) for i, c in enumerate("789456123 0A")}
DIRECTIONS_POSITIONS = {c: (i // 3, i % 3) for i, c in enumerate(" ^A<v>")}


def get_parsed_input(input_path: str):
    lines = read_input_as_lines(input_path)
    return lines


def get_code_as_int(code: str) -> int:
    return int(code[:-1])


def get_steps_counter(chars_to_positions: Dict[Tuple[int, int], str], code: str, i: int = 1):
    prev_x, prev_y = chars_to_positions["A"]
    forbidden_x, forbidden_y = chars_to_positions[" "]
    steps_to_perform_action = Counter()
    for code_char in code:
        next_x, next_y = chars_to_positions[code_char]
        has_passed_next_to_forbidden_cell = (
            next_x == forbidden_x and prev_y == forbidden_y or next_y == forbidden_y and prev_x == forbidden_x
        )
        steps_to_perform_action[(next_x - prev_x, next_y - prev_y, has_passed_next_to_forbidden_cell)] += i
        prev_x, prev_y = next_x, next_y
    return steps_to_perform_action


def get_code_complexity(code: str, repeats: int = 2):
    sol = get_steps_counter(NUMPAD_POSITIONS, code)
    # sol contains the `abstract` actions performed, and how many times
    #  > By `abstract` I mean "twice left and down once". The actual method will be determined by the one simulating those actions,
    #  > as they know best how to optimize the simulation on their end (<^ instead of ^<)
    for i in range(repeats + 1):
        if DEBUG:
            print(f"Code: {code}")
            print(f"Iter = {i}")
        next_sol = Counter()
        for dx, dy, has_passed_next_to_forbidden_cell in sol:
            if DEBUG:
                print(f" > dx, dy, forbidden = {dx, dy, has_passed_next_to_forbidden_cell}")
            # Priority to further away buttons
            path = "<" * -dy + "v" * dx + "^" * -dx + ">" * dy

            # Reversing order if can't press the buttons at the required priority (empty cell)
            #  > For example <<v will turn to v<< (repeating moves beats the priority of buttons)
            reverse_indicator = -1 if has_passed_next_to_forbidden_cell else 1
            if DEBUG:
                print(f" >> Constructed path: {path}")
            path = path[::reverse_indicator] + "A"
            if DEBUG:
                print(f" >> Final path:       {path}")
            steps_to_add = sol[(dx, dy, has_passed_next_to_forbidden_cell)]

            next_counter = get_steps_counter(DIRECTIONS_POSITIONS, path, steps_to_add)
            next_sol += next_counter
            if DEBUG:
                print(f" >> Updated counter:  {next_sol}")
                print("----------------")
        sol = next_sol
    return sol.total()


def solve_part1(input_path: str, expected_output: Optional[int] = None, repeats: int = 2):
    sol = 0
    codes = get_parsed_input(input_path)
    for code in codes:
        sol += get_code_complexity(code, repeats=repeats) * get_code_as_int(code)
    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    solve_part1(input_path, expected_output, 25)


def day21():
    solve_part1(EXAMPLE_PATH, 126384)
    solve_part1(INPUT_PATH, 179444)
    solve_part2(EXAMPLE_PATH, 154115708116294)
    solve_part2(INPUT_PATH, 223285811665866)


if __name__ == "__main__":
    day21()
