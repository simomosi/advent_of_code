'''
https://adventofcode.com/2022/day/17
'''

from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
    
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

class FigureMask:
    def __init__(self, name: str, pixels: list[tuple[int,int]]):
        self.name = name
        self.pixels:set[Point] = set()
        for p in pixels:
            x,y = p
            self.pixels.add(Point(x,y))

mask_figure_dash = FigureMask('-', [(0,0), (1,0), (2,0), (3,0)])
mask_figure_plus = FigureMask('+', [(1,0), (0,1), (1,1), (2,1), (1,2)])
mask_figure_mirrored_l = FigureMask('_|', [(0,0), (1,0), (2,0), (2,1), (2,2)])
mask_figure_stick = FigureMask('|', [(0,0), (0,1), (0,2), (0,3)])
mask_figure_block = FigureMask('[]', [(0,0), (1,0), (0,1), (1,1)])

figures_order = [mask_figure_dash, mask_figure_plus, mask_figure_mirrored_l, mask_figure_stick, mask_figure_block]

def example():
    with open('17/example.txt', 'r') as file:
        jet_pattern = file.readline().strip()
    height = play_tetris(2022, 7, figures_order, jet_pattern)
    assert height == 3068, f"Expected 3068, actual {height}"
    
    height = play_tetris(1_000_000_000_000, 7, figures_order, jet_pattern)
    assert height == 1_514_285_714_288, f"Expected 1_514_285_714_288, actual {height}"
    
def main():
    with open('17/input.txt', 'r') as file:
        jet_pattern = file.readline().strip()
    height = play_tetris(2022, 7, figures_order, jet_pattern)
    print(f"[1] Max weight after 2022 rounds is", height)
    
def play_tetris(round: int, grid_width: int, figures: list[FigureMask], jet_pattern:str):
    fig_pointer = 0
    jp_pointer = 0
    max_height = -1
    cave:set[Point] = set()
    while round > 0:
        print(round)
        fig = figures[fig_pointer]
        rock = initialize_rock(fig, max_height)
        while True:
            direction = jet_pattern[jp_pointer]
            has_moved, rock = apply_jet_direction(rock, direction, grid_width-1, cave)
            is_still_falling, rock = apply_gravity(rock, cave)
            jp_pointer = (jp_pointer+1)%len(jet_pattern)
            if not is_still_falling:
                break
        fig_pointer = (fig_pointer+1)%len(figures)
        max_rock_height = max(p.y for p in rock)
        max_height = max(max_rock_height, max_height)
        for r in rock:
            cave.add(r)
        clean_cave(cave, grid_width)
        round -= 1
    return max_height + 1 # y starts at 0

def initialize_rock(figure: FigureMask, max_height: int) -> set[Point]:
    start = Point(2, max_height+4)
    rock:set[Point] = set()
    for pixel in figure.pixels:
        rock.add(start + pixel)
    return rock

def apply_jet_direction(rock:set[Point], direction: str, grid_width:int, cave: set[Point]) -> tuple[bool, set[Point]]:
    assert direction == '>' or direction == '<'
    mask = Point(1,0) if direction == '>' else Point(-1, 0)
    new_rock:set[Point] = set()
    for old_piece in rock:
        new_piece = old_piece + mask
        if new_piece.x < 0 or new_piece.x > grid_width or new_piece in cave:
            return (False, rock)
        new_rock.add(new_piece)
    return (True, new_rock)

def apply_gravity(rock:set[Point], cave: set[Point]) -> tuple[bool, set[Point]]:
    mask = Point(0, -1)
    new_rock:set[Point] = set()
    for old_piece in rock:
        new_piece = old_piece + mask
        if new_piece.y < 0 or new_piece in cave:
            return (False, rock)
        new_rock.add(new_piece)
    return (True, new_rock)

def clean_cave(cave:set[Point], grid_width: int):
    top_points_y_coordinate:set[int] = set()
    for i in range(grid_width):
        y_coordinate_of_column = {p.y for p in cave if p.x == i}
        if len(y_coordinate_of_column):
            top_points_y_coordinate.add(max(y_coordinate_of_column))    
     
    if len(top_points_y_coordinate) > 0:
        lowest_y = min(top_points_y_coordinate)
        delete_points = {p for p in cave if p.y < lowest_y}
        for d in delete_points:
            cave.remove(d)


if __name__ == '__main__':
    example()
    #main()