from collections import defaultdict
import itertools
import os
from pprint import pprint
import re
from typing import DefaultDict, List, Optional, Set, Tuple
import networkx as nx

from common import DIRECTIONS_RDLU, handle_solution, is_in_board, read_input_as_lines, read_input_as_matrix

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


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
                    for is_cheat_available in (True, False):
                        src, dst = (row, col, is_cheat_available), (row + dr, col + dc, is_cheat_available)
                        edges.append((src, dst, 1))

    G.add_weighted_edges_from(edges)


def get_possible_dsts(
    start: Tuple[int, int], matrix: List[List[str]], directions: Tuple[int, int], steps: int
) -> Set[Tuple[int, int]]:
    dsts = set()
    curr = set()
    row, col = start
    # First step must actually cheat
    rows = len(matrix)
    cols = len(matrix[0])
    for dr, dc in directions:
        if is_in_board(rows, cols, row + dr, col + dc) and matrix[row + dr][col + dc] == "#":
            curr.add((row + dr, col + dc))

    # Maybe for part 2...
    # for step in range(1, steps - 1):
    #     dsts_after_step = []
    #     for (r, c) in curr:
    #         for (dr, dc) in directions:
    #             if is_in_board(matrix, r + dr, c + dc)

    # Last step mustn't cheat
    for r, c in curr:
        for dr, dc in directions:
            if is_cell_habbitable(matrix, r + dr, c + dc):
                dsts.add((r + dr, c + dc))

    dsts.remove(start)
    return dsts


def add_cheating_edges(G: nx.DiGraph, matrix: List[List[str]], max_cheats: int):
    if max_cheats == 0:
        return

    rows = len(matrix)
    cols = len(matrix[0])
    edges = []
    for row in range(rows):
        for col in range(cols):
            if not is_cell_habbitable(matrix, row, col):
                continue

            possible_cheating_dst = get_possible_dsts((row, col), matrix, DIRECTIONS_RDLU, max_cheats)
            for dst in possible_cheating_dst:
                src = (row, col, True)
                actual_dst = (*dst, False)
                edges.append((src, actual_dst, max_cheats))

    G.add_weighted_edges_from(edges)


def construct_graph_from_board(matrix: List[List[str]], max_cheats: int = 0) -> nx.DiGraph:
    G = nx.DiGraph()
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            for is_cheat_available in (True, False):
                G.add_node((row, col, is_cheat_available))

    add_valid_edges(G, matrix)
    add_cheating_edges(G, matrix, max_cheats)
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


def get_parsed_input(input_path: str, max_cheats: int):
    matrix = read_input_as_matrix(input_path)
    start, end = get_start_and_end(matrix)
    return construct_graph_from_board(matrix, max_cheats), (*start, True), (*end, max_cheats == 0)


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
    cheatless_G, start, end = get_parsed_input(input_path, 0)
    cheatless_shortest_path_length = nx.shortest_path_length(cheatless_G, start, end)

    G, start, end = get_parsed_input(input_path, max_cheats)
    shortest_path = nx.shortest_path(G, start, end, weight="weight")
    path_weight = nx.path_weight(G, shortest_path, "weight")
    print(f"path_weight = {path_weight}")
    print(f"cheatless_shortest_path_length = {cheatless_shortest_path_length}")
    while path_weight > 0 and (cheatless_shortest_path_length - path_weight) >= min_discount:
        sol += 1
        print(f"Found improvement of {cheatless_shortest_path_length - path_weight}")
        cheating_edge = find_cheating_edge_from_path(shortest_path)
        G.remove_edge(*cheating_edge)
        shortest_path = nx.shortest_path(G, start, end, weight="weight")
        path_weight = nx.path_weight(G, shortest_path, "weight")

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None, max_cheats: int = 20, min_discount: int = 100):
    sol = 0
    cheatless_G, start, end = get_parsed_input(input_path, 0)
    cheatless_shortest_paths_to_end = nx.shortest_path(cheatless_G, target=end)
    cheatless_shortest_path_length = nx.shortest_path_length(cheatless_G, start, end)
    # print(cheatless_shortest_paths_to_end)
    print(len(cheatless_shortest_paths_to_end))
    # G, start, end = get_parsed_input(input_path, max_cheats)
    # shortest_path = nx.shortest_path(G, start, end, weight="weight")
    # path_weight = nx.path_weight(G, shortest_path, "weight")
    # print(f"path_weight = {path_weight}")
    # print(f"cheatless_shortest_path_length = {cheatless_shortest_path_length}")
    # while path_weight > 0 and (cheatless_shortest_path_length - path_weight) >= min_discount:
    #     sol += 1
    #     print(f"Found improvement of {cheatless_shortest_path_length - path_weight}")
    #     cheating_edge = find_cheating_edge_from_path(shortest_path)
    #     G.remove_edge(*cheating_edge)
    #     shortest_path = nx.shortest_path(G, start, end, weight="weight")
    #     path_weight = nx.path_weight(G, shortest_path, "weight")

    # handle_solution(sol, expected_output)


def day20():
    # solve_part1(EXAMPLE_PATH, min_discount=1, expected_output=44)
    # solve_part1(INPUT_PATH, min_discount=1500)
    # solve_part2(EXAMPLE_PATH, min_discount=1)
    solve_part2(INPUT_PATH)


if __name__ == "__main__":
    day20()
