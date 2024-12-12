from collections import defaultdict
import os
import re
from typing import DefaultDict, Dict, List, Optional, Set, Tuple

from common import handle_solution, is_in_board, read_input_as_lines, read_input_as_matrix

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
EXAMPLE0_PATH = dir_path + os.sep + "example0.txt"
EXAMPLE1_PATH = dir_path + os.sep + "example1.txt"
EXAMPLE2_PATH = dir_path + os.sep + "example2.txt"
EXAMPLE3_PATH = dir_path + os.sep + "example3.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


# class Shape:
#     def __init__(self, letter: str):
#         self.letter = letter
#         self.coords = dict()
#         self.perimeter = 0

#     def add(self, row: int, col: int):
#         self.coords[(row, col)] = True
#         if self.coords.get((row, col - 1)):

#     @property
#     def area(self):
#         return len(self.coords)


class UnionFind:
    def __init__(self):
        self.coord_to_id = dict()  # type: Dict[Tuple[int, int], Tuple[int, int]]
        self.id_to_all_nodes = dict()  # type:Dict[Tuple[int, int], Set[Tuple[int, int]]]

    def _add_aux(self, row: int, col: int, src_row: int, src_col: int):
        src_id = self.coord_to_id[(src_row, src_col)]
        self.coord_to_id[(row, col)] = src_id
        self.id_to_all_nodes[src_id].add((row, col))

    def add(self, matrix: List[List[int]], row: int, col: int):
        rows = len(matrix)
        cols = len(matrix[0])
        if is_in_board(rows, cols, row - 1, col) and matrix[row - 1][col] == matrix[row][col]:
            self._add_aux(row, col, row - 1, col)
            return

        if is_in_board(rows, cols, row, col - 1) and matrix[row][col - 1] == matrix[row][col]:
            self._add_aux(row, col, row, col - 1)
            return

        print(f"Started new shape [{matrix[row][col]}] at {row, col}")
        self.coord_to_id[(row, col)] = (row, col)
        self.id_to_all_nodes[(row, col)] = set((row, col))


def get_parsed_input(input_path: str):
    return read_input_as_matrix(input_path)


# def calculate_shape_perimeter(top, shape: Dict[Tuple[int, int], Set[Tuple[int, int]]]):


def get_new_perimeter(matrix: List[List[int]], letter: str, row: int, col: int):
    new_perimeter = 4
    rows = len(matrix)
    cols = len(matrix[0])
    if is_in_board(rows, cols, row, col - 1) and matrix[row][col - 1] == letter:
        new_perimeter -= 2
    if is_in_board(rows, cols, row - 1, col) and matrix[row - 1][col] == letter:
        new_perimeter -= 2
    print(f" >> New perimeter for {letter} in {row, col}: {new_perimeter}")
    return new_perimeter


def eat_shape_up(matrix: List[List[int]], letter: str, row: int, col: int, visited: Set[Tuple[int, int]]):
    if (row, col) in visited:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    if not is_in_board(rows, cols, row, col):
        return 0
    if matrix[row][col] != letter:
        return 0
    visited.add((row, col))
    added_perimeters = get_new_perimeter(matrix, letter, row, col)
    for r, c in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if is_in_board(rows, cols, row + r, col + c):
            added_perimeters += eat_shape_up(matrix, letter, row + r, col + c, visited)
    return added_perimeters


def eat_all_shapes_up(matrix: List[List[int]]):
    sol = 0
    rows = len(matrix)
    cols = len(matrix[0])
    visited = set()
    for row in range(rows):
        for col in range(cols):
            if (row, col) in visited:
                continue
            letter = matrix[row][col]
            old_visited_len = len(visited)
            perimeter = eat_shape_up(matrix, letter, row, col, visited)
            area = len(visited) - old_visited_len
            if area == 0:
                print(f"No new visited on {row, col}")
                continue
            if perimeter == 0:
                print(f" >>> I think this doesn't make sense...")
            print(f"Ate shape {letter} that starts at {row}, {col}")
            print(f" > Adding {perimeter} * {area} = {perimeter * area}")
            sol += perimeter * area
    return sol


#############################################


def all_neighbors_within_set(row: int, col: int, blocks: Set[Tuple[int, int]]) -> bool:
    ans = True
    for r, c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        ans = ans and (row + r, col + c) in blocks
    return ans


def remove_internal_blocks(blocks: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    new_blocks = blocks.copy()
    for row, col in blocks:
        if all_neighbors_within_set(row, col, blocks):
            new_blocks.remove((row, col))
    return new_blocks


def side_counter(blocks: Set[Tuple[int, int]]) -> int:
    min_row = min([block[0] for block in blocks])
    max_row = max([block[0] for block in blocks])
    min_col = min([block[1] for block in blocks])
    max_col = max([block[1] for block in blocks])
    cnt = 0
    for col in range(min_col, max_col + 1):
        sides_to_right = 0
        sides_to_left = 0
        for row in range(min_row, max_row + 1):
            if (row, col) not in blocks:
                continue
            # Block to left doesn't exist
            if (row, col - 1) not in blocks:
                # block up doesn't exist - new side!
                if (row - 1, col) not in blocks:
                    sides_to_left += 1
                # block up exists, but it has another block to its left - new side!
                elif (row - 1, col - 1) in blocks:
                    sides_to_left += 1
            # Block to right doesn't exist
            if (row, col + 1) not in blocks:
                # block up doesn't exist - new side!
                if (row - 1, col) not in blocks:
                    sides_to_right += 1
                # block up exists, but it has another block to its right - new side!
                elif (row - 1, col + 1) in blocks:
                    sides_to_right += 1
        cnt += sides_to_left + sides_to_right

    return cnt * 2


# def get_sides_count(blocks: Set[Tuple[int, int]]):
#     external_blocks = remove_internal_blocks(blocks)
#     visited = set()


def eat_shape_up_p2(matrix: List[List[int]], letter: str, row: int, col: int, visited: Set[Tuple[int, int]]):
    if (row, col) in visited:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    if not is_in_board(rows, cols, row, col):
        return 0
    if matrix[row][col] != letter:
        return 0
    visited.add((row, col))
    for r, c in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if is_in_board(rows, cols, row + r, col + c):
            eat_shape_up_p2(matrix, letter, row + r, col + c, visited)


def eat_all_shapes_up_p2(matrix: List[List[int]]):
    sol = 0
    rows = len(matrix)
    cols = len(matrix[0])
    all_visited = set()
    shapes_list = []
    for row in range(rows):
        for col in range(cols):
            if (row, col) in all_visited:
                continue
            old_all_visited = all_visited.copy()
            letter = matrix[row][col]
            eat_shape_up_p2(matrix, letter, row, col, all_visited)
            new_visited = all_visited.difference(old_all_visited)
            shapes_list.append(new_visited)
            if letter == "C":
                print("c!!!!CCC")
            sides = side_counter(new_visited)
            area = len(new_visited)
            print(f"Ate shape {letter} that starts at {row}, {col}. Sides: {sides}")
            print(f" > Adding {sides} * {area} = {sides * area}")
            sol += sides * area
    print(shapes_list)
    return sol


# def populate_union_find(matrix: List[List[int]], uf: UnionFind):
#     rows = len(matrix)
#     cols = len(matrix[0])
#     for row in range(rows):
#         for col in range(cols):
#             uf.add(matrix, row, col)


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    # sol = 0
    # uf = UnionFind()
    matrix = get_parsed_input(input_path)
    sol = eat_all_shapes_up(matrix)
    # populate_union_find(matrix, uf)
    # ...

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    matrix = get_parsed_input(input_path)
    sol = eat_all_shapes_up_p2(matrix)

    handle_solution(sol, expected_output)


def day12():
    solve_part1(EXAMPLE0_PATH, 140)
    solve_part1(EXAMPLE1_PATH, 772)
    solve_part1(EXAMPLE_PATH, 1930)
    solve_part1(INPUT_PATH, 1434856)
    solve_part2(EXAMPLE0_PATH, 80)
    solve_part2(EXAMPLE1_PATH, 436)
    solve_part2(EXAMPLE2_PATH, 236)
    solve_part2(EXAMPLE3_PATH, 368)
    solve_part2(INPUT_PATH, 891106)


if __name__ == "__main__":
    day12()
