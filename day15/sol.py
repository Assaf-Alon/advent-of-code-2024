import os
from typing import List, Optional, Set, Tuple

from common import DIRECTIONS_RDLU, handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))


EXAMPLE1_PATH = dir_path + os.sep + "example1.txt"
EXAMPLE2_PATH = dir_path + os.sep + "example2.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def print_board(matrix):
    for line in matrix:
        for c in line:
            print(c, end="")
        print()


def parse_input(input_path: str) -> Tuple[List[List[str]], List[int], int, int]:
    convert_direction_to_index = {">": 0, "v": 1, "<": 2, "^": 3}
    lines = read_input_as_lines(input_path)
    i = 0
    robot_location = [-1, -1]
    while lines[i] != "":
        for j in range(len(lines[i])):
            if lines[i][j] == "@":
                robot_location = [i, j]
        i += 1
    board = [[c for c in line] for line in lines[:i]]

    instructions = []
    for instruction_line in lines[i + 1 :]:
        for instruction in instruction_line:
            instructions.append(convert_direction_to_index[instruction])
    return board, instructions, robot_location[0], robot_location[1]


def find_last_block_in_line(matrix: List[List[str]], bot_location: Tuple[int, int], push_direction: Tuple[int, int]):
    row, col = bot_location
    dr, dc = push_direction
    while matrix[row + dr][col + dc] == "O":
        row += dr
        col += dc

    return (row, col)


def parse_input_p2(input_path: str) -> Tuple[List[List[str]], List[int], int, int]:
    convert_direction_to_index = {">": 0, "v": 1, "<": 2, "^": 3}
    lines = read_input_as_lines(input_path)
    board = []
    i = 0
    robot_location = [-1, -1]
    while lines[i] != "":
        parsed_line = []
        for j in range(len(lines[i])):
            if lines[i][j] == "@":
                robot_location = [i, j * 2]
                parsed_line.append("@")
                parsed_line.append(".")
            elif lines[i][j] == "O":
                parsed_line.append("[")
                parsed_line.append("]")
            else:
                parsed_line.append(lines[i][j])
                parsed_line.append(lines[i][j])
        board.append(parsed_line)
        i += 1
    instructions = []
    for instruction_line in lines[i + 1 :]:
        for instruction in instruction_line:
            instructions.append(convert_direction_to_index[instruction])
    return board, instructions, robot_location[0], robot_location[1]


def get_block_locations(matrix: List[List[str]], partial_location: Tuple[int, int]):
    row, col = partial_location
    if matrix[row][col] == "[":
        assert matrix[row][col + 1] == "]", "Rightside of block is not ]"
        return (row, col), (row, col + 1)
    if matrix[row][col] == "]":
        assert matrix[row][col - 1] == "[", "Leftside of block is not ["
        return (row, col - 1), (row, col)
    raise ValueError("get_block_locations called on non-block")


def can_move_every_block_on_the_way(
    matrix: List[List[str]], bot_location: Tuple[int, int], push_direction: Tuple[int, int]
) -> Optional[Set[Tuple[int, int]]]:
    br, bc = bot_location
    dr, dc = push_direction
    if matrix[br + dr][bc + dc] == ".":
        s = set()
        s.add(bot_location)
        return s
    if matrix[br + dr][bc + dc] == "#":
        return None

    # Need to push horizontically - similar logic to part 1
    if dc != 0:
        check_sideways = can_move_every_block_on_the_way(matrix, (br + dr, bc + dc), push_direction)
        if check_sideways is None:
            return None
        check_sideways.add(bot_location)
        return check_sideways

    # Non-empty, non-edge, must be a block. Recursively check it's possible
    all_blocks_to_push = set()
    block_location_left, block_location_right = get_block_locations(matrix, (br + dr, bc + dc))
    all_blocks_to_push.add(block_location_left)
    all_blocks_to_push.add(block_location_right)
    all_blocks_to_push.add(bot_location)
    left = can_move_every_block_on_the_way(matrix, block_location_left, push_direction)
    if left is None:
        return None
    right = can_move_every_block_on_the_way(matrix, block_location_right, push_direction)
    if right is None:
        return None
    all_blocks_to_push.update(left)
    all_blocks_to_push.update(right)
    return all_blocks_to_push


def can_move(matrix: List[List[str]], bot_location: Tuple[int, int], push_direction: Tuple[int, int]):
    br, bc = bot_location
    dr, dc = push_direction
    return matrix[br + dr][bc + dc] == "."


def is_pushed_at_edge(matrix, row, col, dr, dc):
    return matrix[row + dr][col + dc] == "#"


def sum_boxes_locations(matrix: List[List[str]]):
    sol = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] in ("O", "["):
                sol += (100 * i) + j
    return sol


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    matrix, moves, bot_row, bot_col = parse_input(input_path)
    rows = len(matrix)
    cols = len(matrix[0])
    for move in moves:
        bot_location = (bot_row, bot_col)
        direction = DIRECTIONS_RDLU[move]
        if can_move(matrix, bot_location, direction):
            matrix[bot_row][bot_col] = "."
            bot_row += direction[0]
            bot_col += direction[1]
            matrix[bot_row][bot_col] = "@"
            continue

        last_block = find_last_block_in_line(matrix, (bot_row, bot_col), direction)

        # Catches both cases:
        # - Bot tries to push through the edge
        # - Line of blocks is being pushed through the edge
        if is_pushed_at_edge(matrix, last_block[0], last_block[1], direction[0], direction[1]):
            continue

        row_last_block, col_last_row = last_block
        matrix[row_last_block + direction[0]][col_last_row + direction[1]] = "O"
        matrix[bot_row][bot_col] = "."
        bot_row += direction[0]
        bot_col += direction[1]
        matrix[bot_row][bot_col] = "@"
    sol = sum_boxes_locations(matrix)
    handle_solution(sol, expected_output)


def solve_part2(input_str: str, expected_output: Optional[int] = None):
    matrix, moves, bot_row, bot_col = parse_input_p2(input_str)
    rows = len(matrix)
    cols = len(matrix[0])
    moves_to_dim_and_sign = {0: (1, -1), 1: (0, -1), 2: (1, 1), 3: (0, 1)}
    for move in moves:
        bot_location = (bot_row, bot_col)
        direction = DIRECTIONS_RDLU[move]
        dr, dc = direction
        if can_move(matrix, bot_location, direction):
            matrix[bot_row][bot_col] = "."
            bot_row += dr
            bot_col += dc
            matrix[bot_row][bot_col] = "@"
            continue

        blocks_to_move = can_move_every_block_on_the_way(matrix, bot_location, direction)
        if blocks_to_move is None:
            continue

        def block_key(block):
            dim, sign = moves_to_dim_and_sign[move]
            return block[dim] * sign

        sorted_blocks_to_move = sorted(list(blocks_to_move), key=block_key)
        for block_row, block_col in sorted_blocks_to_move:
            matrix[block_row + dr][block_col + dc] = matrix[block_row][block_col]
            matrix[block_row][block_col] = "."
        matrix[bot_row][bot_col] = "."
        matrix[bot_row + dr][bot_col + dc] = "@"
        (bot_row, bot_col) = bot_row + dr, block_col + dc

        # ad-hoc fix for a vertical push
        if matrix[bot_row][bot_col + 1] == "]":
            matrix[bot_row][bot_col + 1] = "."
        if matrix[bot_row][bot_col - 1] == "[":
            matrix[bot_row][bot_col - 1] = "."

    sol = sum_boxes_locations(matrix)
    handle_solution(sol, expected_output)


def day15():
    solve_part1(EXAMPLE1_PATH, 2028)
    solve_part1(EXAMPLE2_PATH, 10092)
    solve_part2(EXAMPLE2_PATH, 9021)
    solve_part2(INPUT_PATH, 1381446)


if __name__ == "__main__":
    day15()
