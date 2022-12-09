'''
https://adventofcode.com/2022/day/9

[1] The number of positions the tail visits at least once is 6018
[2] The number of positions the tail visits at least once is 2619
'''

class Point():
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


class MovementHandler():
    movements_mask = {'U': (-1, 0), 'D': (1, 0), 'L' : (0, -1), 'R': (0, 1)}

    def __init__(self, points: list[Point]):
        self.points = points
        self.tail_positions_set = {(points[-1].row, points[-1].col)}

    def get_result(self) -> int:
        return len(self.tail_positions_set)

    def move(self, direction: str, steps: int) -> None:
        for i in range(steps):
            self._move_head(direction)
            self._move_body()

    def _move_head(self, direction: str) -> None:
        mask_row, mask_col = self.movements_mask[direction]
        self.points[0].row += mask_row
        self.points[0].col += mask_col

    def _move_body(self) -> None:
        for i in range(1, len(self.points)):
            local_head: Point = self.points[i-1]
            local_tail: Point = self.points[i]
            new_distance = self._get_points_distance(local_head, local_tail)

            if new_distance >= 4:
                self._follow_head(local_head, local_tail)
        self.tail_positions_set.add( (self.points[-1].row, self.points[-1].col) )

    def _get_points_distance(self, a: Point, b: Point) -> int:
        return (a.row - b.row)**2 + (a.col - b.col)**2
    
    def _follow_head(self, head: Point, tail: Point) -> None:
        tail.row += self._get_relative_mask(head.row, tail.row)
        tail.col += self._get_relative_mask(head.col, tail.col)

    def _get_relative_mask(self, head, tail) -> int:
        if head < tail: # Head (coordinate) is UP or LEFT
            return -1
        if head > tail: # Head (coordinate) is DOWN or RIGHT
            return 1
        return 0


def main_mock_part_one():
    head = Point(4, 0)
    tail = Point(4, 0)
    mh = MovementHandler([head, tail])

    instructions_mock_list = ['R 4', 'U 4', 'L 3', 'D 1', 'R 4', 'D 1', 'L 5', 'R 2']
    for direction, steps in [instruction.split() for instruction in instructions_mock_list]:
        mh.move(direction, int(steps))

    result = mh.get_result()
    assert result == 13, f"Expected 13, got {result}"

def main_part_one():
    head = Point(0, 0)
    tail = Point(0, 0)
    mh = MovementHandler([head, tail])

    with open('09/input.txt', 'r') as file:
        for line in file:
            direction, steps = line.strip().split()
            mh.move(direction, int(steps))
    print(f"[1] The number of positions the tail visits at least once is {mh.get_result()}")

def main_mock_part_two():
    knots = [Point(15,11) for i in range(10)]
    mh = MovementHandler(knots)

    instructions_mock_list = ['R 5', 'U 8', 'L 8', 'D 3', 'R 17', 'D 10', 'L 25', 'U 20']
    for direction, steps in [instruction.split() for instruction in instructions_mock_list]:
        mh.move(direction, int(steps))

    result = mh.get_result()
    assert result == 36, f"Expected 36, got {result}"

def main_part_two():
    knots = [Point(0,0) for i in range(10)]
    mh = MovementHandler(knots)

    with open('09/input.txt', 'r') as file:
        for line in file:
            direction, steps = line.strip().split()
            mh.move(direction, int(steps))
    print(f"[2] The number of positions the tail visits at least once is {mh.get_result()}") # 5158 too high

if __name__ == '__main__':
    main_mock_part_one()
    main_part_one()
    main_mock_part_two()
    main_part_two()