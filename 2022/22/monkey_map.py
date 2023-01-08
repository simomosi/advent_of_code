'''
https://adventofcode.com/2022/day/22

Output
[1] The final password is 27492
'''

from typing import NamedTuple

class Coordinate(NamedTuple):
    x: int
    y: int
    
    def __add__(self, _other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + _other.x, self.y + _other.y)


def example():
    board, instructions, max_row, max_col = _read_input('22/example.txt')
    result = find_final_password(board, instructions)
    assert result == 6032, f"Expected 6032, actual is {result}"
    board = instructions = None

def main():
    board, instructions, max_row, max_col = _read_input('22/input.txt')
    result = find_final_password(board, instructions)
    print(f"[1] The final password is {result}") # 209520 Too high
    board = instructions = None

def _read_input(filename) -> tuple[dict[tuple[int,int], str], list[str], int, int]:
    board:dict[tuple[int,int], str] = {}
    y = 1
    x = 1
    max_y = -1
    max_x = -1
    instructions:list[str] = []
    with open(filename, 'r') as file:
        for line in file:
            x = 1
            if line[0].isdigit():
                number_accumulator = ''
                for c in line:
                    if c.isdigit():
                        number_accumulator += c
                    else:
                        instructions.append((number_accumulator))
                        number_accumulator = ''
                        assert c == 'L' or c == 'R' or c == '\n'
                        if c != '\n':
                            instructions.append(c) 
                continue
            for c in line.rstrip():
                if c != ' ':
                    board.setdefault(Coordinate(x, y), c)
                max_x = max(max_x, x)
                x += 1
            max_y = max(max_y, y)
            y += 1
    return board, instructions, max_y, max_x

def find_final_password(board:dict[tuple[int,int], str], instruction:list[str]) -> int :
    y = 1
    x = min(x1 for x1, y1 in board.keys() if y1 == 1)
    pos = Coordinate(x, y)
    
    facing_directions = ['E', 'S', 'W', 'N']
    current_direction = facing_directions.index('E')
    movement_masks = {'N' : Coordinate(0, -1), 'E': Coordinate(1, 0), 'S': Coordinate(0, 1), 'W': Coordinate(-1, 0)}
    turn_directions = {'R': 1, 'L': -1}

    for i in instruction:
        
        if not i.isdigit():
            current_direction = (current_direction + turn_directions[i])%len(facing_directions)
        else:
            steps = int(i)
            while steps > 0:
                direction = facing_directions[current_direction]
                new_pos = pos + movement_masks[direction]
                if new_pos in board:
                    if board.get(new_pos) == '#': # wall
                        break
                    pos = new_pos
                else: # teleport
                    match facing_directions[current_direction]:
                        case 'N':
                            new_y = max(y for x, y in board.keys() if x == pos.x)
                            new_pos = Coordinate(pos.x, new_y)
                        case 'S':
                            new_y = min(y for x, y in board.keys() if x == pos.x)
                            new_pos = Coordinate(pos.x, new_y)
                        case 'E':
                            new_x = min(x for x,y in board.keys() if y == pos.y)
                            new_pos = Coordinate(new_x, pos.y)
                        case 'W':
                            new_x = max(x for x,y in board.keys() if y == pos.y)
                            new_pos = Coordinate(new_x, pos.y)
                    if new_pos in board and board.get(new_pos) != '#':
                        pos = new_pos
                    else:
                        break
                steps -= 1
        
    return compute_password(pos, current_direction)

def compute_password(pos: Coordinate, current_direction:int) -> int :
    return 1000*pos.y + 4*pos.x + current_direction
            

if __name__ == '__main__':
    example()
    main()