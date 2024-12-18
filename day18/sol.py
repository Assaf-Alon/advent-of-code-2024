import os
from typing import List, Optional

from networkx import NetworkXNoPath

from common import DIRECTIONS_RDLU, handle_solution, is_in_board, read_input_as_lines, read_input_as_matrix
import networkx as nx

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

EXAMPLE_BOARD_SIZE = 7
INPUT_BOARD_SIZE = 71


def print_board(matrix):
    for line in matrix:
        for c in line:
            print(c, end="")
        print()


def get_board_after_first_k_blocks(input_path: str, board_size: int, k: int):
    lines = read_input_as_lines(input_path)
    board = [["." for i in range(board_size)] for i in range(board_size)]
    for i in range(k):
        line = lines[i]
        x, y = [int(n) for n in line.split(",")]
        board[y][x] = "#"
    return board


def is_cell_habbitable(matrix: List[List[str]], row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    if not is_in_board(rows, cols, row, col):
        return False
    return matrix[row][col] != "#"


def construct_graph_from_board(matrix: List[List[str]]) -> nx.Graph:
    G = nx.Graph()
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            G.add_node((row, col))

    for row in range(rows):
        for col in range(cols):
            if not is_cell_habbitable(matrix, row, col):
                continue
            for dir_dst in DIRECTIONS_RDLU:
                dst_dr, dst_dc = dir_dst
                if not is_cell_habbitable(matrix, row + dst_dr, col + dst_dc):
                    continue
                src = (row, col)
                dst = (row + dst_dr, col + dst_dc)
                # edges.append((src, dst))
                G.add_edge(src, dst)
    # G.add
    return G


def solve_part1(input_path: str, board_size: int, k: int = 1024, expected_output: Optional[int] = None):
    matrix = get_board_after_first_k_blocks(input_path, board_size, k)
    # print_board(matrix)
    G = construct_graph_from_board(matrix)
    start = (0, 0)
    end = (board_size - 1, board_size - 1)
    shortest_path_length = nx.shortest_path_length(G, start, end)
    sol = shortest_path_length
    return handle_solution(sol, expected_output)


# ---------------------------------------------------------------
# An attempt to do it more efficiently started below (binary search k values),
# but iterating over all k values was enough (ran this while coding)
# Graph construction can also be improved by adding one edge at a time,
# instead of constructing the whole graph again
# ---------------------------------------------------------------
def solve_part2(input_path: str, board_size: int, expected_output: Optional[int] = None):
    lines = read_input_as_lines(input_path)
    min_k = 0 if board_size == EXAMPLE_BOARD_SIZE else 1024
    max_k = len(lines)
    for k in range(min_k, max_k):
        print(f"Trying k = {k}...", end="")
        matrix = get_board_after_first_k_blocks(input_path, board_size, k)
        # print_board(matrix)
        G = construct_graph_from_board(matrix)
        start = (0, 0)
        end = (board_size - 1, board_size - 1)
        try:
            shortest_path_length = nx.shortest_path_length(G, start, end)
            print("[OK]")
        except NetworkXNoPath as e:
            print("[FAILED]")
            sol = lines[k - 1]
            return handle_solution(sol, expected_output)
    raise ValueError("No solution")


# def solve_part2(input_path: str, board_size: int, expected_output: Optional[int] = None):
#     min_k = 0
#     max_k = len(read_input_as_lines(input_path))
#     prev_min_k = min_k
#     prev_max_k = max_k
#     while min_k <= max_k:
#         k = (min_k + max_k) // 2
#         print(f"Trying k = {k}...", end="")
#         matrix = get_board_after_first_k_blocks(input_path, board_size, k)
#         # print_board(matrix)
#         G = construct_graph_from_board(matrix)
#         start = (0, 0)
#         end = (board_size - 1, board_size - 1)
#         try:
#             shortest_path_length = nx.shortest_path_length(G, start, end)
#             print("[OK]")
#             min_k = k + 1
#         except NetworkXNoPath as e:
#             print("[FAILED]")
#             sol = k
#             return handle_solution(sol, expected_output)
#     raise ValueError("No solution")


def day18():
    solve_part1(EXAMPLE_PATH, EXAMPLE_BOARD_SIZE, 12, 22)
    solve_part1(INPUT_PATH, INPUT_BOARD_SIZE, 1024, 280)
    solve_part2(EXAMPLE_PATH, EXAMPLE_BOARD_SIZE, "6,1")
    solve_part2(INPUT_PATH, INPUT_BOARD_SIZE, "28,56")


if __name__ == "__main__":
    day18()
