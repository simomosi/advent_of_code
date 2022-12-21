'''
https://adventofcode.com/2022/day/18

Output
[1] Total surface area: 3500
[2] Exterior surface area: 2048
'''

from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
    z: int
    
    def __add__(self, _other: "Point") -> "Point":
        return Point(self.x + _other.x, self.y + _other.y, self.z + _other.z)

def example():
    points: set[Point] = set()
    with open('18/example.txt', 'r') as file:
        for line in file:
            x,y,z = map(int, line.strip().split(',', maxsplit=2))
            points.add(Point(x,y,z))
    count = count_surface_area(points)
    assert count == 64, f"Expected 64, actual {count}"
    
    count = count_exterior_surface_area(points)
    assert count == 58, f"Expected 58, actual {count}"
    
    
def main():
    points: set[Point] = set()
    with open('18/input.txt', 'r') as file:
        for line in file:
            x,y,z = map(int, line.strip().split(',', maxsplit=2))
            points.add(Point(x,y,z))
    count = count_surface_area(points)
    print(f"[1] Total surface area:", count)
    
    count = count_exterior_surface_area(points)
    print(f"[2] Exterior surface area:", count) # 3200 Too high
    # Note: run dfs on probable trapped air drop

def count_surface_area(points: set[Point]):
    masks: set[Point] = {Point(1,0,0), Point(-1,0,0), Point(0,1,0), Point(0,-1,0), Point(0,0,1), Point(0,0,-1)}
    count = 0
    for p in points:
        for m in masks:
            if p+m not in points:
                count += 1
    return count

def count_exterior_surface_area(points: set[Point]) -> int :
    masks: set[Point] = {Point(1,0,0), Point(-1,0,0), Point(0,1,0), Point(0,-1,0), Point(0,0,1), Point(0,0,-1)}
    min_x = min_y = 0
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    trapped_air_droplets: set[Point] = set() # Cache values not connected with exterior surface
    exterior_air_droplets: set[Point] = set() # Cache values connected with exterior suface
    
    count = 0
    for p in points:
        for m in masks:
            adj = p+m
            if adj not in points and check_path_to_exterior_air(adj, min_x, max_x, min_y, max_y, points, trapped_air_droplets, exterior_air_droplets):
                count += 1
    return count

def check_path_to_exterior_air(
    air_droplet: Point, 
    min_x:int, 
    max_x: int, 
    min_y: int, 
    max_y: int, 
    points: set[Point], 
    trapped_air_droplets: set[Point], 
    exterior_air_droplets: set[Point]
    ) -> bool:
    
    masks: set[Point] = {Point(1,0,0), Point(-1,0,0), Point(0,1,0), Point(0,-1,0), Point(0,0,1), Point(0,0,-1)}
    visited: set[Point] = set()
    result = bfs_to_exterior_air(air_droplet, min_x, max_x, min_y, max_y, masks, points, trapped_air_droplets, exterior_air_droplets, visited)
    if result:
        exterior_air_droplets.update(visited)
    else:
        trapped_air_droplets.update(visited)
    return result
    

def bfs_to_exterior_air(
        air_droplet: Point, 
        min_x:int, 
        max_x: int, 
        min_y: int, 
        max_y: int, 
        masks: set[Point],
        points: set[Point], 
        trapped_air_droplets: set[Point], 
        exterior_air_droplets: set[Point],
        visited: set[Point]):
    
    visited.add(air_droplet)
    if air_droplet in trapped_air_droplets:
        return False
    if air_droplet in exterior_air_droplets:
        return True
    if air_droplet.x < min_x or air_droplet.x > max_x or air_droplet.y < min_y or air_droplet.y > max_y:
        return True # Exterior found
    
    for m in masks:
        adj = air_droplet+m
        if not adj in visited and not adj in points:
            result = bfs_to_exterior_air(adj, min_x, max_x, min_y, max_y, masks, points, trapped_air_droplets, exterior_air_droplets, visited)
            if result:
                return True
    return False

if __name__ == '__main__':
    example()
    main()