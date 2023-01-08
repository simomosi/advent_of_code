'''
https://adventofcode.com/2022/day/23

Output
[1] Empty ground contained in the smallest rectangle: 3762
[2] The first round where Elves does not move is 997
'''

from collections import deque
from typing import NamedTuple

class Coordinate(NamedTuple):
    x:int
    y:int
    
    def __add__(self, _other:"Coordinate") -> "Coordinate":
        return Coordinate(self.x + _other.x, self.y + _other.y)


def example():
    elves = _read_input('23/example.txt')
    empty_ground, _ = move_elves(elves.copy(), 10)
    assert empty_ground == 110, f"Expected 110, actual {empty_ground}"
    _, rounds = move_elves(elves)
    assert rounds == 20, f"Expected 20, actual {rounds}"
    pass

def main():
    elves = _read_input('23/input.txt')
    empty_ground, _ = move_elves(elves.copy(), 10)
    print(f"[1] Empty ground contained in the smallest rectangle: {empty_ground}")
    _, rounds = move_elves(elves)
    print(f"[2] The first round where Elves does not move is {rounds}")
    

def _read_input(filename: str) -> set[Coordinate]:
    elves:set[Coordinate] = set()
    y = 0
    with open(filename, 'r') as file:
        for line in file:
            x = 0
            for c in line.strip():
                if c == '#':
                    elves.add(Coordinate(x, y))
                x += 1
            y += 1
    return elves

def move_elves(elves: set[Coordinate], stop_at:int|None = None):
    directions = deque(['N', 'S', 'W', 'E'])
    movement_coordinate_masks = {
        'N': [Coordinate(0, -1), Coordinate(-1, -1), Coordinate(1, -1)], # N, NW, NE
        'S': [Coordinate(0, 1), Coordinate(-1, 1), Coordinate(1, 1)],  # S, SW, SE
        'W': [Coordinate(-1, 0), Coordinate(-1, -1), Coordinate(-1, 1)], # W, WN, WS
        'E': [Coordinate(1, 0), Coordinate(1, -1), Coordinate(1, 1)] # E, EN, ES
    }
    
    rounds = 0
    while True:
        rounds += 1
        move_elves_map:dict[Coordinate, list[Coordinate]] = {}
        proposed_direction_count:dict[Coordinate, int] = {}
        alone_elves:set[Coordinate] = {elf for elf in elves if is_alone(elf, elves, movement_coordinate_masks)}
        
        if len(alone_elves) == len(elves):
            break
        
        # First Half
        for elf in elves:
            if elf in alone_elves:
                continue
            new_position = propose_move(elf, elves, directions, movement_coordinate_masks)
            if new_position:
                if not new_position in move_elves_map:
                    move_elves_map.setdefault(new_position, [elf])
                else:
                    elves_who_proposed_move = move_elves_map.pop(new_position)
                    elves_who_proposed_move.append(elf)
                    move_elves_map.setdefault(new_position, elves_who_proposed_move)
                if not new_position in proposed_direction_count:
                    proposed_direction_count.setdefault(new_position, 1)
                else:
                    count = proposed_direction_count.pop(new_position)
                    proposed_direction_count.setdefault(new_position, count+1)
                    
        # Second Half
        invalid_positions = [proposed for proposed, count in proposed_direction_count.items() if count > 1]
        for i in invalid_positions:
            move_elves_map.pop(i) # Discard
        for new_position, elves_list in move_elves_map.items():
            elf = elves_list.pop()
            elves.remove(elf)
            elves.add(new_position)
            
        if not stop_at is None and rounds == stop_at:
            break
        directions.append(directions.popleft())
        
    rectangle_min, rectangle_max = find_smallest_rectangle(elves)
    empty_ground = count_empty_ground_in_rectangle(elves, rectangle_min, rectangle_max)
    return empty_ground, rounds
        
    
    
def is_alone(elf:Coordinate, elves:set[Coordinate], movement_coordinate_masks: dict[str, list[Coordinate]]) -> bool:
    return not any(mask for mask_list in movement_coordinate_masks.values() for mask in mask_list if elf+mask in elves)

def propose_move(elf: Coordinate, elves:set[Coordinate], directions:deque[str], movement_coordinate_masks:dict[str, list[Coordinate]]) -> Coordinate|None:
    for d in directions:
        movements = movement_coordinate_masks.get(d)
        if all(elf+m not in elves for m in movements):
            return elf+movements[0] # Main direction
    return None

def find_smallest_rectangle(elves: set[Coordinate]) -> tuple[Coordinate, Coordinate]:
    x_list = {e.x for e in elves}
    smallest_x = min(x_list)
    highest_x = max(x_list)
    y_list = {e.y for e in elves}
    smallest_y = min(y_list)
    highest_y = max(y_list)
    return Coordinate(smallest_x, smallest_y), Coordinate(highest_x, highest_y)
   
def count_empty_ground_in_rectangle(elves: set[Coordinate], rectangle_min:Coordinate, rectangle_max:Coordinate) -> int:
    return (rectangle_max.x - rectangle_min.x +1) * (rectangle_max.y - rectangle_min.y +1) - len(elves)

if __name__ == '__main__':
    example()
    main()