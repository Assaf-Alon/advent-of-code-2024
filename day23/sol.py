from collections import defaultdict
import functools
import os
from typing import Optional, Tuple


from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"
ACTIVE_PATH = INPUT_PATH

DEBUG = True


def get_parsed_input(input_path: str):
    lines = read_input_as_lines(input_path)
    graph = defaultdict(lambda: (set(), set()))
    edges = []
    # graph = defaultdict(lambda: (set(), set()))
    for line in lines:
        n1, n2 = line.split("-")
        edges.append((n1, n2))
        graph[n1][0].add(n2)
        graph[n2][0].add(n1)

        if n2.startswith("t"):
            graph[n1][1].add(n2)

        if n1.startswith("t"):
            graph[n2][1].add(n1)

    return graph, edges


graph, edges = get_parsed_input(ACTIVE_PATH)


def get_t_trio_from_edge(edge: Tuple[str, str]):
    n1, n2 = edge
    achieveable_t1 = graph[n1][1]
    achieveable_t2 = graph[n2][1]

    common = achieveable_t1.intersection(achieveable_t2)
    return [tuple(sorted([n1, n2, t])) for t in common]


def get_3cliques_from_edge(edge: Tuple[str, str]):
    n1, n2 = edge
    achieveables1 = graph[n1][0]
    achieveables2 = graph[n2][0]

    common = achieveables1.intersection(achieveables2)
    return [set([n1, n2, t]) for t in common]


@functools.lru_cache(maxsize=None)
def get_largest_clique(clique_so_far: Tuple[str]):
    largest_clique = clique_so_far
    for n in graph:
        if n in clique_so_far:
            continue
        if all([clique_node in graph[n][0] for clique_node in clique_so_far]):
            new_clique = get_largest_clique(tuple(sorted([*clique_so_far, n])))
            if len(new_clique) > len(largest_clique):
                largest_clique = new_clique
    return largest_clique


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    trios = set()
    for edge in edges:
        new_trios = get_t_trio_from_edge(edge)
        trios.update(new_trios)
    sol = len(trios)
    handle_solution(sol, expected_output)


def print_nodes_degree_histogram(graph):
    hist = defaultdict(lambda: 0)
    for n in graph:
        l = len(graph[n][0])
        hist[l] += 1
    for i in sorted(hist.keys()):
        print(f"{i}: {hist[i]}")


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    graph, edges = get_parsed_input(input_path)
    largest_clique = []
    # Seems like each node is connected to exactly 13 other nodes...
    # print_nodes_degree_histogram(graph)

    for i, edge in enumerate(edges):
        print(f"{i} / {len(edges)}")
        trios = get_3cliques_from_edge(edge)
        for trio in trios:
            clique = get_largest_clique(tuple(sorted(trio)))
            if len(largest_clique) < len(clique):
                largest_clique = clique

    print(f"Largest clique size: {len(largest_clique)}")
    sol = ",".join(sorted(largest_clique))
    handle_solution(sol, expected_output)


def day23():
    if ACTIVE_PATH == EXAMPLE_PATH:
        solve_part1(EXAMPLE_PATH, 7)
        solve_part2(EXAMPLE_PATH, "co,de,ka,ta")
    if ACTIVE_PATH == INPUT_PATH:
        solve_part1(INPUT_PATH, 1215)
        solve_part2(INPUT_PATH, "bm,by,dv,ep,ia,ja,jb,ks,lv,ol,oy,uz,yt")


if __name__ == "__main__":
    day23()
