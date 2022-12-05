'''

'''

import re
move_regex = re.compile('move (\d+) from (\d+) to (\d+)')

def main_part_one():
    stacks = get_stacks_configuration()
    with open('05/input.txt', 'r') as file:
        for i in range(9):
            print(file.readline(), end='')
        move = file.readline()
        print(f"###########")
        move = file.readline()
        while move != '':
            # print(move, end='')
            moves_number, start, end = map(int, [m for m in move_regex.match(move).groups()])
            while moves_number > 0:
                move_crate(stacks, start-1, end-1)
                moves_number -= 1
            move = file.readline()
        print(f"[1] Crate on top of each stack with CrateMover 9000: ", end='')
        for s in stacks:
            print(s[-1], end='')

def main_part_two():
    stacks = get_stacks_configuration()
    with open('05/input.txt', 'r') as file:
        for i in range(9):
            print(file.readline(), end='')
        move = file.readline()
        print(f"###########")
        move = file.readline()
        while move != '':
            # print(move, end='')
            moves_number, start, end = map(int, [m for m in move_regex.match(move).groups()])
            move_multiple_crates(stacks, moves_number, start-1, end-1)
            move = file.readline()
        print(f"[2] Crate on top of each stack with CrateMover 9001: ", end='')
        for s in stacks:
            print(s[-1], end='')

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

def move_crate(stacks, stack_from, stack_to):
    crate = stacks[stack_from].pop()
    stacks[stack_to].append(crate)

def move_multiple_crates(stacks, moves_number, stack_from, stack_to):
    temp_stack = []
    while moves_number > 0:
        crate = stacks[stack_from].pop()
        temp_stack.append(crate)
        moves_number -= 1
    while len(temp_stack) > 0:
        stacks[stack_to].append(temp_stack.pop())

if __name__ == '__main__':
    main_part_one()
    main_part_two()
    print()