from math import inf
import os
from typing import List, Optional, Tuple

from common import DIRECTIONS_RDLU, handle_solution, is_in_board, read_input_as_lines, read_input_as_matrix
import networkx as nx

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE1_PATH = dir_path + os.sep + "example1.txt"
EXAMPLE2_PATH = dir_path + os.sep + "example2.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def is_cell_habbitable(matrix: List[List[str]], row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    if not is_in_board(rows, cols, row, col):
        return False
    return matrix[row][col] != "#"


def get_start_and_end(matrix: List[List[str]]):
    start = None
    end = None
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == "S":
                start = (row, col)
            if matrix[row][col] == "E":
                end = (row, col)
            if start and end:
                return start, end
    raise ValueError("Bad matrix!")


def construct_graph_from_board(matrix: List[List[str]]) -> nx.Graph:
    G = nx.Graph()
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            for dir in DIRECTIONS_RDLU:
                G.add_node((row, col, dir))

    edges = []
    for row in range(rows):
        for col in range(cols):
            if not is_cell_habbitable(matrix, row, col):
                continue
            for dir_dst in DIRECTIONS_RDLU:
                dst_dr, dst_dc = dir_dst
                if not is_cell_habbitable(matrix, row + dst_dr, col + dst_dc):
                    continue
                for dir_src in DIRECTIONS_RDLU:
                    if dir_src[0] + dir_dst[0] == 0 and dir_src[1] + dir_dst[1] == 0:
                        continue
                    weight = 1 + 1000 * int(dir_src != dir_dst)
                    src = (row, col, dir_src)
                    dst = (row + dst_dr, col + dst_dc, dir_dst)
                    edges.append((src, dst, weight))
    G.add_weighted_edges_from(edges)
    return G


def get_path_weight(path: List[Tuple[int, int, Tuple[int, int]]]):
    weight = 0
    for i in range(1, len(path)):
        src_dir = path[i - 1][2]
        dst_dir = path[i][2]
        weight += 1 + (1000 * int(src_dir != dst_dir))
    return weight


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    matrix = read_input_as_matrix(input_path)
    s, e = get_start_and_end(matrix)
    sr, sc = s
    er, ec = e
    start = (sr, sc, DIRECTIONS_RDLU[0])
    shortest = inf
    G = construct_graph_from_board(matrix)
    for end in [(er, ec, direction) for direction in DIRECTIONS_RDLU]:
        p = nx.shortest_path(G, start, end, "weight")
        path_weight = get_path_weight(p)
        shortest = min(shortest, path_weight)
    sol = shortest
    return handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    matrix = read_input_as_matrix(input_path)
    s, e = get_start_and_end(matrix)
    sr, sc = s
    er, ec = e
    start = (sr, sc, DIRECTIONS_RDLU[0])
    best_locations = set()
    shortest_path_weight = solve_part1(input_path)
    G = construct_graph_from_board(matrix)
    for end in [(er, ec, direction) for direction in DIRECTIONS_RDLU]:
        all_paths = nx.all_shortest_paths(G, source=start, target=end, weight="weight")
        for path in all_paths:
            if get_path_weight(path) != shortest_path_weight:
                continue
            nodes_on_path = [(node[0], node[1]) for node in path]
            best_locations = best_locations.union(set(nodes_on_path))

    sol = len(best_locations)
    handle_solution(sol, expected_output)


def day16():
    solve_part1(EXAMPLE1_PATH, 7036)
    solve_part1(EXAMPLE2_PATH, 11048)
    solve_part1(INPUT_PATH, 111480)
    solve_part2(EXAMPLE1_PATH, 45)
    solve_part2(EXAMPLE2_PATH, 64)
    solve_part2(INPUT_PATH, 529)


if __name__ == "__main__":
    day16()
