'''
https://adventofcode.com/2022/day/14

Output
[1] Number of sand grains come to rest is  799
[2] Number of sand grains come to rest (with a floor) is 29076
'''

def example():
    path_points: list[tuple[int,int]] = []
    rocks: set[tuple[int, int]] = set()
    with open('14/example_input.txt', 'r') as file:
        for line in file:
            for points in line.split('->'):
                row, col = map(int, points.strip().split(',', maxsplit=2))
                path_points.append((row, col))
            new_path = build_rocks_path(path_points)
            rocks.update(new_path)
            path_points = []
            
    abyss_height = max(row for _, row in rocks)
    sand_grains = pour_sand(rocks, abyss_height)
    assert sand_grains == 24, f"Expected 24 sand grains, actual {sand_grains}"
    
    outmost_left = min(col for col, _ in rocks)
    outmost_right = max(col for col, _ in rocks)
    floor_path = build_rocks_path([(outmost_left-10, abyss_height+2), (outmost_right+10, abyss_height+2)])
    rocks.update(floor_path)
    sand_grains = pour_sand(rocks, 1000)
    assert sand_grains == 93, f"Expected 93 sand grains with floor, actual {sand_grains}"
    
def main():
    path_points: list[tuple[int,int]] = []
    rocks: set[tuple[int, int]] = set()
    with open('14/input.txt', 'r') as file:
        for line in file:
            for points in line.split('->'):
                row, col = map(int, points.strip().split(',', maxsplit=2))
                path_points.append((row, col))
            new_path = build_rocks_path(path_points)
            rocks.update(new_path)
            path_points = []
    abyss_height = max(row for _, row in rocks)
    sand_grains = pour_sand(rocks, abyss_height)
    print(f"[1] Number of sand grains come to rest is ", sand_grains)
    
    outmost_left = min(col for col, _ in rocks)
    outmost_right = max(col for col, _ in rocks)
    floor_path = build_rocks_path([(outmost_left-1000, abyss_height+2), (outmost_right+1000, abyss_height+2)])
    rocks.update(floor_path)
    sand_grains = pour_sand(rocks, 1000)
    print(f"[2] Number of sand grains come to rest (with a floor) is", sand_grains)
        

def build_rocks_path(points: list[tuple[int, int]]) -> set[tuple[int, int]]:
    rocks: set[tuple[int, int]] = set()
    for i in range(1, len(points)):
        prev = points[i-1]
        next = points[i]
        while True:
            rocks.add(prev)
            if prev == next:
                break
            if prev[0] != next[0]:
                step = 1 if next[0] > prev[0] else -1
                prev = (prev[0]+step, prev[1])
            if prev[1] != next[1]:
                step = 1 if next[1] > prev[1] else -1
                prev = (prev[0], prev[1]+step)
    return rocks
            
# NB: row and col are inverted!
def pour_sand(rocks: set[tuple[int, int]], abyss_height: tuple[int, int]) -> bool:
    sand_grains: set[tuple[int, int]] = set()
    start_point = (500,0)
    number_of_grains = 0
    while add_sand_unit(rocks, sand_grains, start_point, abyss_height):
        number_of_grains += 1
    return number_of_grains

def add_sand_unit(rocks: set[tuple[int, int]], sand_grains: set[tuple[int, int]], unit: tuple[int, int], abyss_height: tuple[int, int]) -> bool:
    col, row = unit
    while True:
        if row > abyss_height:
            return False # Abyss
        if not (col, row+1) in rocks and not (col, row+1) in sand_grains:
            row += 1
        elif not (col-1, row+1) in rocks and not (col-1, row+1) in sand_grains:
            row += 1
            col += -1
        elif not (col+1, row+1) in rocks and not (col+1, row+1) in sand_grains:
            row += 1
            col += 1
        else:
            if (col, row) == unit and unit in sand_grains: # Start point
                return False
            sand_grains.add((col, row))
            return True # Rest

if __name__ == '__main__':
    example()
    main()