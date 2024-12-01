from typing import Optional


def handle_solution(solution: any, expected_output: Optional[int] = None):
    if expected_output:
        assert expected_output == solution
        print("[OK]")
        return

    print(solution)
