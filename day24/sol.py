from collections import defaultdict
from copy import deepcopy
import functools
from math import inf
from operator import and_, or_, xor
import os
from pprint import pprint
from typing import DefaultDict, Dict, List, Optional, Set, Tuple


from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
EXAMPLE2_PATH = dir_path + os.sep + "example2.txt"
EXAMPLE_EVAL_PATH = dir_path + os.sep + "evals.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"
ACTIVE_PATH = INPUT_PATH

DEBUG = False


class Node:
    pass


def parse_example_evals() -> Dict[str, str]:
    lines = read_input_as_lines(EXAMPLE_EVAL_PATH)
    d = dict()
    for line in lines:
        k, v = line.split(": ")
        d[k] = v
    return d


class Node:
    def __init__(self, name: str, value: Optional[int] = None):
        self.name = name
        self.inputs = []
        self.outputs = set()
        self.value = value

    def __repr__(self):
        return f"Node {self.name} with {len(self.inputs)} inputs and {len(self.outputs)} outputs. Eval={self.value}"

    def add_inputs(self, input1: str, input2: str, eval: str):
        self.inputs = [input1, input2]
        self.eval_method = eval

    def add_output(self, output_name: str):
        self.outputs.add(output_name)

    def remove_input(self, input_name: str):
        self.inputs.remove(input_name)

    def evaluate(self, graph: DefaultDict[str, Node]):
        if len(self.inputs) == 0:
            return
        w1, w2 = self.inputs
        assert graph[w1].value is not None
        assert graph[w2].value is not None

        self.value = Node.evaluate_wire(graph[w1].value, graph[w2].value, self.eval_method)
        if DEBUG:
            print(f"Evaluating {self.name} as the {self.eval_method} of the previous {w1}, {w2}")
            print(f" >> whose values are {graph[w1].value, graph[w2].value}")
            print(f" >> output: {graph[self.name].value}")

    @staticmethod
    def evaluate_wire(v1: str, v2: str, eval: str):
        operators = {"AND": and_, "OR": or_, "XOR": xor}
        v1, v2 = int(v1), int(v2)
        assert eval in operators.keys()
        return str(operators[eval](v1, v2))


def add_wire(graph: Dict[str, Node], wire: str):
    w, v = wire.split(": ")
    n = Node(name=w, value=v)
    graph[w] = n


def add_gate(graph: DefaultDict[str, Node], gate: str):
    w1, g, w2, _, o = gate.split(" ")
    if graph.get(o) is None:
        graph[o] = Node(name=o)
    if graph.get(w1) is None:
        graph[w1] = Node(name=w1)
    if graph.get(w2) is None:
        graph[w2] = Node(name=w2)
    graph[o].add_inputs(w1, w2, g)
    graph[w1].add_output(o)
    graph[w2].add_output(o)


def get_parsed_input(input_path: str) -> Tuple[DefaultDict[str, Node], List[str]]:
    lines = read_input_as_lines(input_path)
    # graph = defaultdict(lambda: (set()))
    graph = defaultdict(lambda x: (Node(name=x)))
    parsing_wires = True
    for line in lines:
        if line == "":
            parsing_wires = False
            continue

        if parsing_wires:
            add_wire(graph, line)
        else:
            add_gate(graph, line)
    outputs = [n for n in graph.keys() if n.startswith("z")]
    return graph, sorted(outputs, reverse=True)


def do_topological_sort_step(graph: DefaultDict[str, Node], sinks: List[str], sorted_keys: List[str]):
    assert sinks
    curr_sink = sinks[-1]
    sinks.pop()

    sorted_keys.append(curr_sink)
    for t in graph[curr_sink].outputs:
        graph[t].remove_input(curr_sink)
        if len(graph[t].inputs) == 0:
            sinks.append(t)


def topological_sort(graph: DefaultDict[str, Node]) -> List[str]:
    g = deepcopy(graph)
    sinks = []
    sorted_keys = []
    # Initialize sinks
    for n in g.keys():
        if len(g[n].inputs) == 0:
            sinks.append(n)

    while len(sinks) > 0:
        do_topological_sort_step(g, sinks, sorted_keys)

    return sorted_keys


def get_outcome_in_binary(graph: DefaultDict[str, Node], outputs: List[str]):
    sol = ""
    sorted_node_keys = topological_sort(graph)
    for n_key in sorted_node_keys:
        graph[n_key].evaluate(graph)
    for b in outputs:
        sol += graph[b].value
    return sol


def solve_part1(input_path: str, expected_output: Optional[int] = None):
    graph, outputs = get_parsed_input(input_path)
    sol = get_outcome_in_binary(graph, outputs)

    decimal_sol = int(sol, 2)
    return handle_solution(decimal_sol, expected_output)


def expected_addition_result_binary(graph: DefaultDict[str, Node], output_length: int):
    x = sorted([n for n in graph.keys() if n.startswith("x")], reverse=True)
    y = sorted([n for n in graph.keys() if n.startswith("y")], reverse=True)
    in1, in2 = "", ""
    for n1, n2 in zip(x, y):
        in1 += graph[n1].value
        in2 += graph[n2].value
    res = int(in1, 2) + int(in2, 2)
    res_bin = bin(res)[2:]
    res_bin = "0" * (output_length - len(res_bin)) + res_bin
    print(len(x), len(res_bin))
    return res_bin


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    sol = ""
    graph, outputs = get_parsed_input(input_path)
    expected = expected_addition_result_binary(graph, len(outputs))
    actual = get_outcome_in_binary(graph, outputs)
    print(f"expected: {expected}")
    print(f"actual:   {actual}")


def day24():
    solve_part1(EXAMPLE_PATH, 2024)
    solve_part1(INPUT_PATH, 61495910098126)
    # solve_part2(EXAMPLE_PATH)
    # solve_part2(INPUT_PATH)


if __name__ == "__main__":
    day24()
