from typing import List, Optional


def handle_solution(solution: any, expected_output: Optional[int] = None):
    if expected_output:
        assert expected_output == solution, f"Expected solution is {expected_output}. Got {solution}"
        print("[OK]")
        return

    print(solution)
    return solution


def read_input_as_matrix(input_path: str) -> List[List[str]]:
    with open(input_path) as f:
        lines = f.readlines()
        return [list(line.removesuffix("\n")) for line in lines]


def read_input_as_string(input_path: str) -> str:
    with open(input_path) as f:
        return f.read()


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
        return [line.removesuffix("\n") for line in lines]
