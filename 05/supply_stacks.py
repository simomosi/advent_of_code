'''
https://adventofcode.com/2022/day/3

Output
[1] Crate on top of each stack with CrateMover 9000: CWMTGHBDW
[2] Crate on top of each stack with CrateMover 9001: SSCGWJCRB

Let n be the number of crates
Let m be the number of instructions

Time Complexity:
- Read m instructions
- Each instruction moves at most n crates
O(m*n)

Space Complexity: O(m) + O(n)
'''

from io import TextIOWrapper
import re
move_regex = re.compile('move (\d+) from (\d+) to (\d+)')

class Instruction:
    def __init__(self, moves_number, start, end):
        self.moves_number = moves_number
        self.start = start
        self.end = end

def main_part_one() -> None:
    stacks = get_stacks_configuration()
    with open('05/input.txt', 'r') as file:
        stacks = read_configuration(file)
        move = file.readline() # Empty line
        move = file.readline()
        while move != '':
            moves_number, start, end = map(int, (m for m in move_regex.match(move).groups()))
            instruction = Instruction(moves_number, start-1, end-1)
            move_crate(stacks, instruction)
            move = file.readline()
    print(f"[1] Crate on top of each stack with CrateMover 9000: {get_solution(stacks)}")

def main_part_two() -> None:
    with open('05/input.txt', 'r') as file:
        stacks = read_configuration(file)
        move = file.readline() # Empty line
        move = file.readline()
        while move != '':
            moves_number, start, end = map(int, (m for m in move_regex.match(move).groups()))
            instruction = Instruction(moves_number, start-1, end-1)
            move_multiple_crates(stacks, instruction)
            move = file.readline()
    print(f"[2] Crate on top of each stack with CrateMover 9001: {get_solution(stacks)}")

def read_configuration(file: TextIOWrapper):
    # Discard first 10 lines
    for i in range(9):
        config_row = file.readline()
        # print(config_row, end='') # Crates Configuration
    return get_stacks_configuration()

'''
                [M]     [V]     [L]
[G]             [V] [C] [G]     [D]
[J]             [Q] [W] [Z] [C] [J]
[W]         [W] [G] [V] [D] [G] [C]
[R]     [G] [N] [B] [D] [C] [M] [W]
[F] [M] [H] [C] [S] [T] [N] [N] [N]
[T] [W] [N] [R] [F] [R] [B] [J] [P]
[Z] [G] [J] [J] [W] [S] [H] [S] [G]
 1   2   3   4   5   6   7   8   9
'''
def get_stacks_configuration():
    stacks = []
    stacks.append(['Z', 'T', 'F', 'R', 'W', 'J', 'G'])
    stacks.append(['G', 'W', 'M'])
    stacks.append(['J', 'N', 'H', 'G'])
    stacks.append(['J', 'R', 'C', 'N', 'W'])
    stacks.append(['W', 'F', 'S', 'B', 'G', 'Q', 'V', 'M'])
    stacks.append(['S', 'R', 'T', 'D', 'V', 'W', 'C'])
    stacks.append(['H', 'B', 'N', 'C', 'D', 'Z', 'G', 'V'])
    stacks.append(['S', 'J', 'N', 'M', 'G', 'C'])
    stacks.append(['G', 'P', 'N', 'W', 'C', 'J', 'D', 'L'])
    return stacks

def move_crate(stacks, instruction: Instruction) -> None:
    moves_number = instruction.moves_number
    while moves_number > 0:
        crate = stacks[instruction.start].pop()
        stacks[instruction.end].append(crate)
        moves_number -= 1

def move_multiple_crates(stacks, instruction: Instruction) -> None:
    temp_stack = []
    moves_number = instruction.moves_number
    while moves_number > 0:
        crate = stacks[instruction.start].pop()
        temp_stack.append(crate)
        moves_number -= 1
    while len(temp_stack) > 0:
        stacks[instruction.end].append(temp_stack.pop())

def get_solution(stacks):
    solution = ''
    for s in stacks:
        solution += s[-1]
    return solution

if __name__ == '__main__':
    main_part_one()
    main_part_two()