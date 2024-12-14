from collections import defaultdict
from functools import reduce
from operator import mul
import os
import re
from time import sleep
from typing import DefaultDict, List, Optional, Set, Tuple, Dict

from common import (
    DIRECTIONS_RDLU,
    add_2d_vectors,
    handle_solution,
    is_in_board,
    multiply_2d_vector,
    read_input_as_lines,
    string_to_image,
)

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

LINE_PATTERN = r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)"

ROWS, COLS = 101, 103
E_ROWS, E_COLS = 11, 7

"""
  0 1 2 3 4 ..
  ---------------------
0 |
1 |
2 |
3 |
4 |
..|
"""


class UnionFind:
    def __init__(self, rows, cols):
        self.parent = {}  # Map from coordinate to its parent
        self.rank = {}  # Map from coordinate to its rank
        self.size = {}  # Map from root to size of the group
        self.rows = rows
        self.cols = cols

    def find(self, coord):
        # Path compression
        if self.parent[coord] != coord:
            self.parent[coord] = self.find(self.parent[coord])
        return self.parent[coord]

    def union(self, coord1, coord2):
        # Union by rank with size tracking
        root1 = self.find(coord1)
        root2 = self.find(coord2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
                self.size[root1] += self.size[root2]
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
                self.size[root2] += self.size[root1]
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
                self.size[root1] += self.size[root2]

    def add(self, row, col):
        coord = (row, col)
        if coord not in self.parent:
            self.parent[coord] = coord
            self.rank[coord] = 0
            self.size[coord] = 1

        # Check and union with neighbors
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nr, nc = row + dr, col + dc
            if is_in_board(self.rows, self.cols, nr, nc) and (nr, nc) in self.parent:
                self.union(coord, (nr, nc))

    def get_group_size(self, row, col):
        coord = (row, col)
        if coord in self.parent:
            root = self.find(coord)
            return self.size[root]
        return 0  # If the coordinate is not in any group


def print_board(rows: int, cols: int, locations: List[Tuple[int, int]]):
    for col in range(cols):
        for row in range(rows):
            if (row, col) in locations:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def parse_input(_input: List[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    positions = []
    velocities = []
    for line in _input:
        mtch = re.search(LINE_PATTERN, line)
        if mtch is None:
            raise ValueError(f"Failed matching line {line}")
        positions.append((int(mtch.group(1)), int(mtch.group(2))))
        velocities.append((int(mtch.group(3)), int(mtch.group(4))))
    return positions, velocities


def get_parsed_input(input_path: str):
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def get_quadrant(row: int, col: int, rows: int, cols: int):
    if row < rows // 2:
        if col < cols // 2:
            return 1
        if col >= (cols // 2) + 1:
            return 2
    if row >= (rows // 2) + 1:
        if col < cols // 2:
            return 3
        if col >= (cols // 2) + 1:
            return 4
    return 0


def solve_part1(input_path: str, expected_output: Optional[int] = None, rows: int = ROWS, cols: int = COLS):
    steps = 100
    positions, velocities = get_parsed_input(input_path)
    total_in_each_quadrant = [0, 0, 0, 0, 0]  # First index is for coordinates not in any quadrant
    for pos, v in zip(positions, velocities):
        new_pos = add_2d_vectors(pos, multiply_2d_vector(v, steps))
        row, col = new_pos[0] % rows, new_pos[1] % cols
        quadrant = get_quadrant(row, col, rows, cols)
        total_in_each_quadrant[quadrant] += 1

    sol = reduce(mul, total_in_each_quadrant[1:])
    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None, rows: int = ROWS, cols: int = COLS):
    positions, velocities = get_parsed_input(input_path)
    max_iters = 10000
    sol = 0
    for i in range(0, max_iters):
        # if i % 1000 == 0:
        #     print(f" {i} / {max_iters}")
        uf = UnionFind(rows, cols)

        end_positions = []
        for pos, v in zip(positions, velocities):
            new_pos = add_2d_vectors(pos, multiply_2d_vector(v, i))
            row, col = new_pos[0] % rows, new_pos[1] % cols
            end_positions.append((row, col))
            uf.add(row, col)

        for size in uf.size.values():
            if size >= 25:
                sol = i
                # print_board(rows, cols, end_positions)
                # print(f"WOAH! size = {size} for i={i}")
                # input("Press enter to continue...")
                # break

    handle_solution(sol, expected_output)


def day14():
    solve_part1(EXAMPLE_PATH, rows=E_ROWS, cols=E_COLS, expected_output=12)
    solve_part1(INPUT_PATH, expected_output=222062148)
    # solve_part2(EXAMPLE_PATH, rows=E_ROWS, cols=E_COLS)
    solve_part2(INPUT_PATH, 7520)


if __name__ == "__main__":
    day14()
