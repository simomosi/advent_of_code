'''
https://adventofcode.com/2022/day/24

Output
[1] The fewest number of minutes required to avoid the blizzards and reach the goal is 299
[2] The fewest number of minutes required to reach the goal, go back to the start, then reach the goal again is 899
'''

from typing import NamedTuple
from enum import Enum
from collections import deque

class Direction(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3
    
    @staticmethod
    def from_char(char: str) -> "Direction":
        match char:
            case '^':
                return Direction.UP
            case '>':
                return Direction.RIGHT
            case 'v':
                return Direction.DOWN
            case '<':
                return Direction.LEFT
            case other:
                raise Exception(f"Unknown direction type: {other}")

class Point(NamedTuple):
    x:int
    y:int
    
    def __add__(self, _other: "Point") -> "Point":
        return Point(self.x + _other.x, self.y + _other.y)
    
class Blizzard:
    def __init__(self, dir:Direction, pos:Point):
        self.dir = dir
        self.pos = pos

class BlizzardHandler():
    movement_mask = {
        Direction.UP: Point(0,-1),
        Direction.DOWN: Point(0,1),
        Direction.LEFT: Point(-1,0),
        Direction.RIGHT: Point(1,0)
    }
    
    def __init__(self, blizzards:set[Blizzard], rows, columns):
        self.blizzards = blizzards
        self.rows = rows
        self.columns = columns
        self.blizzards_positions_lookup:dict[int, set[Point]] = {}
        
    def is_point_occupied_by_blizzard(self, point:Point, time:int) -> bool:
        if not self.blizzards_positions_lookup.get(time, None):
            self.advance_blizzards()
            self.blizzards_positions_lookup.clear()
            self.build_lookup(time)
        return point in self.blizzards_positions_lookup.get(time)

    def advance_blizzards(self):
        step = 1
        for b in self.blizzards:
            new_pos = None
            match b.dir:
                case Direction.RIGHT:
                    new_x = (b.pos.x -1 + step) % (self.columns -2) +1
                    new_pos = Point(new_x, b.pos.y)
                case Direction.LEFT:
                    new_x = (b.pos.x -1 - step) % (self.columns -2) +1
                    new_pos = Point(new_x, b.pos.y)
                case Direction.DOWN:
                    new_y = (b.pos.y -1 + step) % (self.rows -2) +1
                    new_pos = Point(b.pos.x, new_y)
                case Direction.UP:
                    new_y = (b.pos.y -1 - step) % (self.rows -2) +1
                    new_pos = Point(b.pos.x, new_y)
            b.pos = new_pos
            
    def build_lookup(self, time:int):
        lookup:set[Point] = set(b.pos for b in self.blizzards)
        self.blizzards_positions_lookup.setdefault(time, lookup)
        
    
def example():
    start, end, blizzards, walls, rows, columns = _read_input('24/example.txt')
    blizzard_handler = BlizzardHandler(blizzards, rows, columns)
    minutes = reach_goal(start, end, walls, blizzard_handler)
    assert minutes == 18, f"Expected 18, actual {minutes}"
    
    minutes_back = reach_goal(end, start, walls, blizzard_handler, minutes)
    minutes_again = reach_goal(start, end, walls, blizzard_handler, minutes_back)
    assert minutes_again == 54, f"Expected 54, actual {minutes_again}"

def main():
    start, end, blizzards, walls, rows, columns = _read_input('24/input.txt')
    blizzard_handler = BlizzardHandler(blizzards, rows, columns)
    minutes = reach_goal(start, end, walls, blizzard_handler)
    print(f"[1] The fewest number of minutes required to avoid the blizzards and reach the goal is", minutes)
    
    minutes_back = reach_goal(end, start, walls, blizzard_handler, minutes)
    minutes_again = reach_goal(start, end, walls, blizzard_handler, minutes_back)
    print(f"[2] The fewest number of minutes required to reach the goal, go back to the start, then reach the goal again is", minutes_again)

def _read_input(filename:str) -> tuple[Point, Point, set[Blizzard], set[Point], int, int]:
    start = end = None
    blizzards: set[Blizzard] = set()
    walls:set[Point] = set()
    with open(filename, 'r') as file:
        lines = file.readlines()
        rows = len(lines)
        columns = len(lines[0].strip())
        start = Point(lines[0].index('.') , 0)
        end = Point(lines[-1].index('.'), rows-1)
        for y in range(rows):
            for x in range(columns):
                character = lines[y][x]
                if character in ('<', '>', '^', 'v'):
                    b = Blizzard(Direction.from_char(character), Point(x,y))
                    blizzards.add(b)
                elif character == '#':
                    walls.add(Point(x,y))
        lines = None
        
    walls.add(start + Point(0,-1))  # Top of start point
    walls.add(end + Point(0,1))     # Bottom of end point
    return start, end, blizzards, walls, rows, columns

def reach_goal(start:Point, end:Point, walls:set[Point], blizzard_handler:BlizzardHandler, start_time:int = 0) -> int:
    directions = (Point(0,1),   # Down
                  Point(1,0),   # Right
                  Point(0,-1),  # Up
                  Point(-1,0),  # Left
                  Point(0,0))   # Wait
    minutes = start_time
    visited: set[tuple[Point,int]] = set((start, minutes))
    queue:deque[tuple[Point, int]] = deque([(start, minutes)])
    while queue:
        current, minutes = queue.popleft()
        next_minute = minutes+1
        if current == end:
            break
        for dir in directions:
            adj = current + dir
            if not adj in walls and not (adj, next_minute) in visited and not blizzard_handler.is_point_occupied_by_blizzard(adj, next_minute):
                visited.add((adj, next_minute))
                queue.append((adj, next_minute))
      
    return minutes
    

if __name__ == '__main__':
    example()
    main()