'''
https://adventofcode.com/2022/day/15

Output
[1] Possible beacons on row 2000000 is 4919281
'''

import re
from typing import NamedTuple, Iterable
from itertools import chain

input_coordinate_re = re.compile('x=(-?\d+), y=(-?\d+)')

class Point(NamedTuple):
    x: int
    y: int

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

    height = 10
    impossible_beacons = find_impossible_beacon_positions(sensor_beacon_couples, height)
    impossible_beacons_on_row_10 = len([p.x for p in impossible_beacons if p.y == height])
    assert impossible_beacons_on_row_10 == 26, f"Expected 26, actual {impossible_beacons_on_row_10}"
    
    impossible_beacons = impossible_beacons_on_row_10 = None
    undetected_beacons = find_undetected_beacon(sensor_beacon_couples, 0, 20)
    assert undetected_beacons and undetected_beacons.x == 14 and undetected_beacons.y == 11
    
def main():
    sensor_beacon_couples: set[tuple[Point, Point]] = set()
    with open('15/input.txt', 'r') as file:
        for line in file:
            l = line.split(':')
            sx, sy = map(int, input_coordinate_re.search(l[0]).groups())
            sensor = Point(sx, sy)
            bx, by = map(int, input_coordinate_re.search(l[1]).groups())
            beacon = Point(bx, by)
            sensor_beacon_couples.add((sensor, beacon))

    height = 2000000
    impossible_beacons = find_impossible_beacon_positions(sensor_beacon_couples, height)
    impossible_beacons_on_row_2000000 = len([p.x for p in impossible_beacons if p.y == height])
    print(f"[1] On row {height} the number of position which cannot contain a beacon is {impossible_beacons_on_row_2000000}")
    impossible_beacons = impossible_beacons_on_row_2000000 = None
    
    undetected_beacons = find_undetected_beacon(sensor_beacon_couples, 0, 4000000)
    print(f"Sequence", undetected_beacons.x*4000000 + undetected_beacons.y)
    
def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

def find_impossible_beacon_positions(sensor_beacon_couples: set[tuple[Point, Point]], y: int) -> set[Point]:
    sensors: set[Point] = {s for s, _ in sensor_beacon_couples}
    beacons: set[Point] = {b for _, b in sensor_beacon_couples}
    
    impossible_beacons: set[Point] = set()
    for s, b in sensor_beacon_couples:
        closest_point_to_s_in_y = Point(s.x, y)
        if manhattan_distance(s, closest_point_to_s_in_y) > manhattan_distance(s,b):
            continue
        for r in get_x_solutions(s, b, y):
            rmin, rmax = r
            for x in range(rmin, rmax):
                p = Point(x,y)
                if not p in sensors and not p in beacons:
                    impossible_beacons.add(p)
    return impossible_beacons

def get_x_solutions(sensor: Point, beacon: Point, y: int) -> list[tuple[int, int]]:
    # I solved the following inequality for Px
    # | Sx - Px| + |Sy - Py| <= d_sb
    distance = manhattan_distance(sensor, beacon)
    ranges = []
    # print(f"For row {y} possible x are:")
    
    solution_one_left = sensor.x - distance + abs(sensor.y - y)
    solution_one_right = sensor.x
    ranges.append((solution_one_left, solution_one_right + 1))
    # if solution_one_right >= solution_one_left:
        # print(f"[1] {solution_one_left} <= x <= {solution_one_right}")
        
    solution_two_left = sensor.x
    solution_two_right = distance - abs(sensor.y - y) + sensor.x
    ranges.append((solution_two_left + 1, solution_two_right + 1))
    # if solution_two_left < solution_two_right:
    #     print(f"[2] {solution_two_left} < x <= {solution_two_right}")
    return ranges

def find_undetected_beacon(sensor_beacon_couples: set[tuple[Point, Point]], min_coordinate: int, max_coordinate: int) -> Point:
    sensors: set[Point] = {s for s, _ in sensor_beacon_couples}
    beacons: set[Point] = {b for _, b in sensor_beacon_couples}
    
    candidate_points: dict[int, list[Point]] = {}
    for s,b in sensor_beacon_couples:
        perimeter = find_perimeter_points(s, b)
        for p in perimeter:
            if p.x < min_coordinate or p.x > max_coordinate:
                continue
            if p.y < min_coordinate or p.y > max_coordinate:
                continue
            if p in sensors or p in beacons:
                continue
            candidate_points.setdefault(p.y, [])
            candidate_points.get(p.y).append(p)
    perimeter = None
    for height in candidate_points.keys():
        print(f"Analyzing points at height {height}")
        all_ranges_row_y: list[tuple[int,int]] = []
        for s, b in sensor_beacon_couples:
            ranges_of_x_for_s_b = get_x_solutions(s, b, height)
            for r in ranges_of_x_for_s_b:
                all_ranges_row_y.append(r)
            del ranges_of_x_for_s_b
                    
        for p in candidate_points.get(height):
            x_in_range = False
            for r in all_ranges_row_y:
                left, right = r
                if left <= p.x <= right+1:
                    x_in_range = True
                    break
            if not x_in_range:
                print(f"Point found!")
                print(p)
                return p


def find_perimeter_points(sensor: Point, beacon: Point) -> set[Point]:
    distance = manhattan_distance(sensor, beacon)
    perimeter: set[Point] = set()
    
    c: Point = Point(sensor.x - distance - 1, sensor.y)
    masks = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    for m in masks:
        xm, ym = m
        for d in range(distance+1):
            c = Point(c.x + xm, c.y + ym)
            perimeter.add(c)
    return perimeter
        
    

if __name__ == '__main__':
    #example()
    main()