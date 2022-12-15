'''
https://adventofcode.com/2022/day/15
'''

import re

input_coordinate_re = re.compile('x=(-?\d+), y=(-?\d+)')

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def example():
    sensor_beacon_couples: set[tuple[Point, Point]] = set()
    with open('15/example_input.txt', 'r') as file:
        for line in file:
            l = line.split(':')
            sx, sy = map(int, input_coordinate_re.search(l[0]).groups())
            sensor = Point(sx, sy)
            bx, by = map(int, input_coordinate_re.search(l[1]).groups())
            beacon = Point(bx, by)
            sensor_beacon_couples.add((sensor, beacon))

    possible_beacons = compute_possible_beacon_positions(sensor_beacon_couples)
    assert len(possible_beacons) == 26, f"Expected 26, actual {len(possible_beacons)}"
    pass

def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

def compute_possible_beacon_positions(sensor_beacon_couples: set[tuple[Point, Point]]) -> set[Point]:
    sensors: set[Point] = {s for s, _ in sensor_beacon_couples}
    beacons: set[Point] = {b for _, b in sensor_beacon_couples}

    union_points = sensors | beacons
    min_x = min(p.x for p in union_points)
    max_x = max(p.x for p in union_points)
    min_y = min(p.y for p in union_points)
    max_y = max(p.y for p in union_points)
    union_points = None

    possible_beacons: set[Point] = set()
    for s, b in sensor_beacon_couples:
        distance = manhattan_distance(s, b)
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                p = Point(x, y)
                if (p not in sensors 
                and p not in beacons
                and manhattan_distance(s, p) <= distance):
                    possible_beacons.add(p)
    return possible_beacons

if __name__ == '__main__':
    example()