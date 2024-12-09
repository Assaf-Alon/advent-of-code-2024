from collections import defaultdict
from math import inf
import os
import re
from typing import DefaultDict, List, Optional, Tuple

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def parse_input(_input: List[str]):
    pass


def get_parsed_input(input_path: str):
    _input = read_input_as_lines(input_path)
    return parse_input(_input)


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    start = 0
    input_string = read_input_as_lines(input_path)[0]
    end = len(input_string) - 1
    end_block_index = end // 2
    curr_block_for_checksum = 0
    remaining_blocks_in_end = int(input_string[end])
    while start < end:
        start_block_length = int(input_string[start])
        start_block_index = start // 2
        end_block_index = end // 2
        free_block_length = int(input_string[start + 1])
        # Add start_block to checksum
        for _ in range(start_block_length):
            sol += curr_block_for_checksum * start_block_index
            curr_block_for_checksum += 1

        # Fill free block
        for _ in range(free_block_length):
            # Skip if no free block
            while remaining_blocks_in_end == 0:  # I think while should be sufficient here
                end -= 2
                remaining_blocks_in_end = int(input_string[end])

            if start >= end:
                break

            end_block_index = end // 2
            remaining_blocks_in_end -= 1
            sol += curr_block_for_checksum * end_block_index
            curr_block_for_checksum += 1

        start += 2

    while remaining_blocks_in_end:
        sol += curr_block_for_checksum * end_block_index
        curr_block_for_checksum += 1
        remaining_blocks_in_end -= 1
    handle_solution(sol, expected_output)


# -------------------------------------------------------------


def get_free_blocks_by_size(arr: List[int]) -> List[List[int]]:
    free_blocks_by_size = [list() for _ in range(10)]
    block_index_start = 0
    for i in range(1, len(arr), 2):
        prev = arr[i - 1]
        curr = arr[i]
        block_index_start += prev
        free_blocks_by_size[curr].append(block_index_start)
        block_index_start += curr
    return free_blocks_by_size


def get_diff_in_blocks(arr: List[int], curr_block: int):
    if curr_block == 0:
        return 0

    return arr[curr_block - 1] + arr[curr_block - 2]


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    input_string = read_input_as_lines(input_path)[0]
    arr = [int(c) for c in input_string]
    new_arr = [(int(c), i // 2) if i % 2 == 0 else (int(c), -1) for i, c in enumerate(input_string)]
    free_blocks_by_size = get_free_blocks_by_size(arr)  # type: List[List[int]]
    total_blocks = sum(arr)
    curr_block_location = total_blocks - arr[-1]

    checksum_filled = 0
    checksum_stayed = 0
    indexes_moved = set()

    # Move blocks around
    for i in range(len(arr) - 1, -1, -2):
        index_block_to_move = i // 2
        size_block_to_move = arr[i]
        size_to_fill = -1
        min_index_to_fill = inf
        for size in range(size_block_to_move, 10):
            if free_blocks_by_size[size] and free_blocks_by_size[size][0] < min_index_to_fill:
                min_index_to_fill = free_blocks_by_size[size][0]
                size_to_fill = size

        if min_index_to_fill >= curr_block_location:
            curr_block_location -= get_diff_in_blocks(arr, i)
            continue
        curr_block_location -= get_diff_in_blocks(arr, i)

        assert size_to_fill > 0

        indexes_moved.add(index_block_to_move)
        free_blocks_by_size[size_to_fill].pop(0)
        if size_block_to_move < size_to_fill:
            free_blocks_by_size[size_to_fill - size_block_to_move].insert(0, min_index_to_fill + size_block_to_move)
            free_blocks_by_size[size_to_fill - size_block_to_move].sort()

        for current_block_pos in range(min_index_to_fill, min_index_to_fill + size_block_to_move):
            checksum_filled += current_block_pos * index_block_to_move

    curr_block_for_checksum = 0
    for i in range(0, len(new_arr), 2):
        start_block_length = arr[i]
        start_block_index = i // 2
        assert start_block_index >= 0
        assert start_block_length >= 0
        if start_block_index in indexes_moved:
            curr_block_for_checksum += start_block_length + (0 if i == len(arr) - 1 else arr[i + 1])
            continue

        # Add start_block to checksum
        for _ in range(start_block_length):
            checksum_stayed += curr_block_for_checksum * start_block_index
            curr_block_for_checksum += 1
        curr_block_for_checksum += 0 if i == len(arr) - 1 else arr[i + 1]

    sol = checksum_filled + checksum_stayed

    handle_solution(sol, expected_output)


def day09():
    solve_part1(EXAMPLE_PATH, 1928)
    solve_part1(INPUT_PATH, 6356833654075)
    solve_part2(EXAMPLE_PATH, 2858)
    solve_part2(INPUT_PATH, 6389911791746)


if __name__ == "__main__":
    day09()
