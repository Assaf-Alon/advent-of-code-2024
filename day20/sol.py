import os
import re
from typing import Dict, List, Optional, Set, Tuple
import networkx as nx

from common import DIRECTIONS_RDLU, handle_solution, is_in_board, read_input_as_lines, read_input_as_matrix

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

DEBUG = False


def is_cell_habbitable(matrix: List[List[str]], row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    if not is_in_board(rows, cols, row, col):
        return False
    return matrix[row][col] != "#"


def add_valid_edges(G: nx.DiGraph, matrix: List[List[str]]):
    rows = len(matrix)
    cols = len(matrix[0])
    edges = []
    for row in range(rows):
        for col in range(cols):
            if not is_cell_habbitable(matrix, row, col):
                continue

            for dr, dc in DIRECTIONS_RDLU:
                if is_cell_habbitable(matrix, row + dr, col + dc):
                    src, dst = (row, col), (row + dr, col + dc)
                    edges.append((src, dst))

    G.add_edges_from(edges)


def get_possible_dsts(start: Tuple[int, int], matrix: List[List[str]], steps: int) -> Set[Tuple[int, int]]:
    dsts = set()
    curr = set()
    curr.add(start)

    row, col = start

    for dr in range(-steps, steps + 1):
        for dc in range(-steps, steps + 1):
            if abs(dr) + abs(dc) > steps:
                continue
            if not is_cell_habbitable(matrix, row + dr, col + dc):
                continue
            dst = row + dr, col + dc
            dsts.add(dst)

    dsts.remove(start)
    return dsts


def get_cheating_edges(matrix: List[List[str]], max_cheats: int) -> List[Tuple[int, int, int]]:
    rows = len(matrix)
    cols = len(matrix[0])
    edges = []
    for row in range(rows):
        for col in range(cols):
            if not is_cell_habbitable(matrix, row, col):
                continue

            src = (row, col)
            possible_cheating_dst = get_possible_dsts(src, matrix, max_cheats)
            for dst in possible_cheating_dst:
                man_dist = abs(src[0] - dst[0]) + abs(src[1] - dst[1])
                edges.append((src, dst, man_dist))
    if DEBUG:
        print(len(edges))
    return edges


def add_cheating_edges(G: nx.DiGraph, matrix: List[List[str]], max_cheats: int):
    if max_cheats == 0:
        return
    edges = get_cheating_edges(matrix, max_cheats)
    G.add_weighted_edges_from(edges)


def construct_graph_from_board(matrix: List[List[str]]) -> nx.DiGraph:
    G = nx.DiGraph()
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            G.add_node((row, col))

    add_valid_edges(G, matrix)
    return G


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


def get_parsed_input(input_path: str):
    matrix = read_input_as_matrix(input_path)
    start, end = get_start_and_end(matrix)
    return construct_graph_from_board(matrix), start, end


def find_cheating_edge_from_path(
    path: List[Tuple[int, int, bool]]
) -> Tuple[Tuple[int, int, bool], Tuple[int, int, bool]]:
    for i in range(1, len(path)):
        src = path[i - 1]
        dst = path[i]
        if src[2] != dst[2]:
            return (src, dst)


def solve_part1(input_path: str, expected_output: Optional[int] = None, max_cheats: int = 2, min_discount: int = 100):
    sol = 0
    matrix = read_input_as_matrix(input_path)
    cheatless_G, start, end = get_parsed_input(input_path)
    if DEBUG:
        print(cheatless_G)
    shortest_paths_to_end = nx.shortest_path_length(cheatless_G, target=end)
    shortest_paths_from_start = nx.shortest_path_length(cheatless_G, source=start)
    shortest_path_length = nx.shortest_path_length(cheatless_G, start, end)

    cheating_edges = get_cheating_edges(matrix, max_cheats)
    progress_indicator = 0
    for i, edge in enumerate(cheating_edges):
        if DEBUG and i // 100 != progress_indicator:
            progress_indicator += 1
            print(f"{i} / {len(cheating_edges)}")
        edge_src = edge[0]
        edge_dst = edge[1]
        weight = shortest_paths_from_start[edge_src] + edge[2] + shortest_paths_to_end[edge_dst]
        sol += int(shortest_path_length - weight >= min_discount)

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None, min_discount: int = 100):
    solve_part1(input_path=input_path, expected_output=expected_output, max_cheats=20, min_discount=min_discount)


def day20():
    solve_part1(EXAMPLE_PATH, min_discount=1, expected_output=44)
    solve_part1(INPUT_PATH, 1518)
    solve_part2(EXAMPLE_PATH, min_discount=50, expected_output=285)
    solve_part2(INPUT_PATH, expected_output=1032257)


if __name__ == "__main__":
    day20()
