'''
https://adventofcode.com/2022/day/2

Output
[1] The total score with strategy #1 is 9651
[2] The total score with strategy #2 is 10560

Part 1
Let n be the number of matches
Time Complexity: O(n)
Space Complexity: O(1)

Part 2
Time Complexity: O(n)
Space Complexity: O(1)
'''

from enum import Enum

class Shapes(Enum):
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2

shapes = (Shapes.ROCK, Shapes.PAPER, Shapes.SCISSORS)
# shapes[i % 3] loses against shapes[(i+1) % 3]
# shapes[i % 3] wins agains shapes[(i-1) % 3]

shape_normalizer = {
    'A': Shapes.ROCK,
    'X': Shapes.ROCK,
    'B': Shapes.PAPER,
    'Y': Shapes.PAPER,
    'C': Shapes.SCISSORS,
    'Z': Shapes.SCISSORS,
}

shape_score = {
    Shapes.ROCK: 1, 
    Shapes.PAPER: 2, 
    Shapes.SCISSORS: 3
}


class Outcome(Enum):
    LOSE = 0,
    DRAW = 1,
    WIN = 2

outcome_normalizer = {
    'X': Outcome.LOSE,
    'Y': Outcome.DRAW,
    'Z': Outcome.WIN
}

match_outcome_score = {
    Outcome.WIN: 6,
    Outcome.DRAW: 3,
    Outcome.LOSE: 0
}


def compute_score(opponent_shape: Shapes, my_shape: Shapes) -> int:
    return shape_score[my_shape] + _get_round_outcome_score(opponent_shape, my_shape)

def _get_round_outcome_score(opponent_shape: Shapes, my_shape: Shapes) -> int:
    if opponent_shape == my_shape:
        return match_outcome_score[Outcome.DRAW]
    
    my_shape_index = shapes.index(my_shape)
    opponent_shape_index = shapes.index(opponent_shape)
    if my_shape_index == (opponent_shape_index+1)%3:
        return match_outcome_score[Outcome.WIN]
    return match_outcome_score[Outcome.LOSE]

def get_shape_based_on_round_outcome(opponent_shape: Shapes, round_outcome: Outcome)-> Shapes:
    opponent_shape_index = shapes.index(opponent_shape)
    if round_outcome == Outcome.DRAW:
        my_shape = shapes[opponent_shape_index] 
    elif round_outcome == Outcome.LOSE:
        my_shape =  shapes[(opponent_shape_index-1)%3] 
    elif round_outcome == Outcome.WIN:
        my_shape = shapes[(opponent_shape_index+1)%3]
    return my_shape

def main_part_one():
    total_score = 0
    with open('02/input.txt', 'r') as file:
        for line in file:
            opponent_shape = shape_normalizer[line[0]]
            my_shape = shape_normalizer[line[2]]
            total_score += compute_score(opponent_shape, my_shape)
    print(f"[1] The total score with strategy #1 is {total_score}")

def main_part_two():
    total_score = 0
    with open('02/input.txt', 'r') as file:
        for line in file:
            opponent_shape = shape_normalizer[line[0]]
            outcome = outcome_normalizer[line[2]]
            my_shape = get_shape_based_on_round_outcome(opponent_shape, outcome)
            total_score += compute_score(opponent_shape, my_shape)
    print(f"[2] The total score with strategy #2 is {total_score}")

if __name__ == '__main__':
    main_part_one()
    main_part_two()