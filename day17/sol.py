from operator import xor
import os
from typing import List, Optional

from common import handle_solution, read_input_as_lines

dir_path = os.path.dirname(os.path.realpath(__file__))

EXAMPLE_PATH = dir_path + os.sep + "example.txt"
EXAMPLE2_PATH = dir_path + os.sep + "example2.txt"
INPUT_PATH = dir_path + os.sep + "input.txt"

DEBUG = False


def parse_input(_input: List[str]):
    A = int(_input[0].split(" ")[-1])
    B = int(_input[1].split(" ")[-1])
    C = int(_input[2].split(" ")[-1])
    tape = _input[-1].split(" ")[-1]
    tape = [int(n) for n in tape.split(",")]

    return tape, [A, B, C]



def get_parsed_input(input_path: str):
    lines = read_input_as_lines(input_path)
    return parse_input(lines)


def get_combo_operand(tape: List[int], registers: List[int], ip: int):
    assert len(registers) == 3
    operand = tape[ip + 1]
    if 0 <= operand <= 3:
        return operand
    assert 4 <= operand <= 6

    return registers[operand - 4]
    

def dv_base(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]] = None, out_index: Optional[int] = 0):
    combo = get_combo_operand(tape, registers, ip)
    numerator = registers[0]
    denominator = 2 ** combo
    registers[out_index] = numerator // denominator
    return ip + 2

def adv(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]] = None):
    ret = dv_base(tape, registers, ip, out_tape, 0)
    if DEBUG:
        print(f"adv called, registers = {registers}")
    return ret

def bxl(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]]):
    operand = tape[ip + 1]
    registers[1] = xor(registers[1], operand)
    if DEBUG:
        print(f"bxl called, registers = {registers}")
    return ip + 2

def bst(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]]):
    combo = get_combo_operand(tape, registers, ip) % 8
    registers[1] = combo
    if DEBUG:
        print(f"bst called, registers = {registers}")
    return ip + 2

def jnz(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]]):
    if registers[0] == 0:
        return ip + 2
    operand = tape[ip + 1]
    if DEBUG:
        print(f"jnz called, registers = {registers}")
    return operand

def bxc(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]]):
    operand = tape[ip + 1] # Ignored, legacy
    registers[1] = xor(registers[1], registers[2])
    if DEBUG:
        print(f"bxc called, registers = {registers}")
    return ip + 2

def out(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]]):
    combo = get_combo_operand(tape, registers, ip)
    out_tape.append(combo % 8)
    if DEBUG:
        print(f"out called, registers = {registers}")
    return ip + 2

def bdv(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]] = None):
    ret = dv_base(tape, registers, ip, out_tape, 1)
    if DEBUG:
        print(f"bdv called, registers = {registers}")
    return ret

def cdv(tape: List[int], registers: List[int], ip: int, out_tape: Optional[List[int]] = None):
    ret = dv_base(tape, registers, ip, out_tape, 2)
    if DEBUG:
        print(f"cdv called, registers = {registers}")
    return ret

def run_machine(tape: List[int], registers: List[int]):
    operators = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    ip = 0
    out_tape = []
    while ip < len(tape):
        operator = operators[tape[ip]]
        ip = operator(tape, registers, ip, out_tape)
        if DEBUG and ip < len(tape) and tape[ip] == 3:
            print(f"tape: {tape}")
            print(f"registers: {registers}")
            print(f"ip: {ip}")
            print(f"out tape: {out_tape}")
            input("Press enter to continue...")
    return ",".join([str(n) for n in out_tape])

def solve_part1(input_path: str, expected_output: Optional[int] = None):
    sol = 0
    tape, registers = get_parsed_input(input_path)
    sol = run_machine(tape, registers)
    handle_solution(sol, expected_output)

def run_machine_iteration(tape: List[int], registers: List[int]):
    operators = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    ip = 0
    out_tape = []
    while ip < len(tape) and tape[ip] != 3:
        operator = operators[tape[ip]]
        ip = operator(tape, registers, ip, out_tape)
    assert len(out_tape) == 1
    return out_tape[0]

def get_possible_a_values_for_final_iteration(tape: List[int]):
    possible_values = []
    for a in range(1, 8):
        registers = [a, 0, 0]
        if run_machine_iteration(tape, registers) == 0:
            possible_values.append(a)
    if DEBUG:
        print(f"Bootstrap - {possible_values}")
    return possible_values


def solve_part2(input_path: str, expected_output: Optional[int] = None):
    tape, registers = get_parsed_input(input_path)
    good_a_values = set(get_possible_a_values_for_final_iteration(tape))
    output_order = tape[::-1][1:]
    for next_output in output_order:
        if DEBUG:
            print(f"!!!! Starting iteration looking for {next_output} with {good_a_values}")
        if not good_a_values:
            raise ValueError("NO MORE GOOD A VALUES :(")
        next_good_a_values = set()
        for good_a in good_a_values:
            if DEBUG:
                print(f" >> Scanning for optionals for {good_a}")
            for diff in range(8):
                curr_iteration_a = (good_a * 8) + diff
                registers = [curr_iteration_a, 0, 0]
                if DEBUG:
                    print(f" >>> Adding diff {diff}, running {registers}")
                output = run_machine_iteration(tape, registers)
                if DEBUG:
                    print(f" >>> output = {output}")
                if output == next_output:
                    if DEBUG:
                        print(f" > A = {curr_iteration_a}, output = {output}, !!!NICE!!!")
                    registers = [curr_iteration_a, 0, 0]
                    run_machine(tape, registers)
                    next_good_a_values.add(curr_iteration_a)
                if DEBUG:
                    print(f"A = {curr_iteration_a}, output = {output}, expected = {next_output}")
            good_a_values = next_good_a_values


    sol = min(good_a_values)
    handle_solution(sol, expected_output)


def day17():
    solve_part1(EXAMPLE_PATH, "4,6,3,5,6,3,5,2,1,0")
    solve_part1(INPUT_PATH, "5,1,4,0,5,1,0,2,6")
    solve_part2(EXAMPLE2_PATH, 117440)
    solve_part2(INPUT_PATH, 202322936867370)


if __name__ == "__main__":
    day17()




# Register A: 65804993
# Register B: 0
# Register C: 0

# operators = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
#
# # bst (Store Combo [value of A] at B)
# # bxl (XOR B's result with 1 (add / subtract 1))
# # cdv (2^A // 5 --> C)
# Program: 2,4, # bst   B = A mod 8
#          1,1, # bxl   B = (A mod 8) xor 1
#          7,5, # cdv   C = A >> B         // C = (A >> (A mod 8 xor 1))
#          1,4, # bxl   B = B XOR 4        // (A mod 8) XOR 5
#          0,3, # adv   A = A >> 3         // 
#          4,5, # bxc   B = B XOR C        // (A mod 8) XOR (A >> (A mod 8 xor 1))  XOR 5
#          5,5, # out   OUTPUT B mod 8
#          3,0  # jnz   if A != 0, return to start

