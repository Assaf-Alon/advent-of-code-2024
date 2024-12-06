from collections import defaultdict
from copy import deepcopy
import copy
import os
import re
from typing import DefaultDict, List, Optional, Tuple
import graphlib

from common import handle_solution

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
        return lines


def parse_input(input: List[str]):
    is_reading_edges = True
    edges = []
    updates = []
    for line in input:
        if line == "\n":
            is_reading_edges = False
            continue

        if is_reading_edges:
            line_match = re.match(r"(\d+)\|(\d+)", line)
            edges.append((line_match.group(1), line_match.group(2)))
        else:
            updates.append(line.replace("\n", "").split(","))
    return edges, updates


def construct_graph_from_edges(edges):
    vertices = set([edge[0] for edge in edges] + [edge[1] for edge in edges])
    graph = {vertex: set() for vertex in vertices}
    for edge in edges:
        graph[edge[0]].add(edge[1])
    return graph


def should_add_edge(source, target, nodes):
    return source in nodes and target in nodes


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    input_lines = read_input_as_lines(input_path)
    edges, updates = parse_input(input_lines)

    for update in updates:
        temp_edges = []  # copy.copy(edges)
        temp_nodes = set()
        for i in range(1, len(update)):
            source, target = update[i - 1], update[i]
            temp_edges.append((source, target))
            temp_nodes.add(source)
            temp_nodes.add(target)

        for source, target in edges:
            if should_add_edge(source, target, temp_nodes):
                temp_edges.append((source, target))

        graph = construct_graph_from_edges(temp_edges)
        topological_sorted_graph = graphlib.TopologicalSorter(graph)
        try:
            tuple(topological_sorted_graph.static_order())  # Check the topological order is alright
            middle = len(update) // 2
            sol += int(update[middle])
        except graphlib.CycleError as e:
            # print(e)
            pass

    handle_solution(sol, expected_output)


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    input_lines = read_input_as_lines(input_path)
    edges, updates = parse_input(input_lines)

    for update in updates:
        original_relevant_edges = []
        temp_edges = []  # copy.copy(edges)
        temp_nodes = set()
        for i in range(1, len(update)):
            source, target = update[i - 1], update[i]
            temp_edges.append((source, target))
            temp_nodes.add(source)
            temp_nodes.add(target)

        for source, target in edges:
            if should_add_edge(source, target, temp_nodes):
                original_relevant_edges.append((source, target))
                temp_edges.append((source, target))

        graph = construct_graph_from_edges(temp_edges)
        topological_sorted_graph = graphlib.TopologicalSorter(graph)
        try:
            tuple(topological_sorted_graph.static_order())  # Check the topological order is alright
            continue
        except graphlib.CycleError as e:
            pass

        try:
            # print("!!!!!!!!!!!!! YEAHGGGGGGGGGGGGGGGG")
            # print(original_relevant_edges)
            graph = construct_graph_from_edges(original_relevant_edges)
            topological_sorted_graph = graphlib.TopologicalSorter(graph)
            fixed_update = tuple(topological_sorted_graph.static_order())
            middle = len(fixed_update) // 2
            sol += int(fixed_update[middle])
        except graphlib.CycleError as e:
            print("!!!!!!!!!!!!!!! NOOOOOOOOOOOOO")
            exit(1)

    handle_solution(sol, expected_output)


def day05():
    solve_part1(EXAMPLE_PATH, 143)
    solve_part1(INPUT_PATH, 6384)
    solve_part2(EXAMPLE_PATH, 123)
    solve_part2(INPUT_PATH, 5353)


if __name__ == "__main__":
    day05()
