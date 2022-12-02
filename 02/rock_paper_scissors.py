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

shapes = ('R', 'P', 'S')
# shapes[i % 3] loses against shapes[(i+1) % 3]
# shapes[i % 3] wins agains shapes[(i-1) % 3]

def normalize_shape(shape):
    if shape == 'A' or shape == 'X':
        return 'R' # Rock
    if shape == 'B' or shape == 'Y':
        return 'P' # Paper
    if shape == 'C' or shape == 'Z':
        return 'S' # Scissors
    raise Exception('Wrong input')

def compute_score(opponent_shape, my_shape):
    return _get_shape_score(my_shape) + _get_round_outcome_score(opponent_shape, my_shape)

def _get_shape_score(shape):
    if shape == 'R':
        return 1
    if shape == 'P':
        return 2
    if shape == 'S':
        return 3
    raise Exception(f"Shape not found: {shape}")

def _get_round_outcome_score(opponent_shape, my_shape):
    if opponent_shape == my_shape: # Draw
        return 3
    my_shape_index = shapes.index(my_shape)
    opponent_shape_index = shapes.index(opponent_shape)
    if my_shape_index == (opponent_shape_index+1)%3: # Win
        return 6
    return 0 # Lose

def get_shape_based_on_round_outcome(opponent_shape, round_outcome):
    opponent_shape_index = shapes.index(opponent_shape)
    if round_outcome == 'Y': # Draw
        my_shape = shapes[opponent_shape_index] 
    elif round_outcome == 'X': # Lose
        my_shape =  shapes[(opponent_shape_index-1)%3] 
    elif round_outcome == 'Z': # Win
        my_shape = shapes[(opponent_shape_index+1)%3]
    return my_shape

def main_part_one():
    total_score = 0
    with open('02/input.txt', 'r') as file:
        for line in file:
            opponent_shape = normalize_shape(line[0])
            my_shape = normalize_shape(line[2])
            total_score += compute_score(opponent_shape, my_shape)
    print(f"[1] The total score with strategy #1 is {total_score}")

def main_part_two():
    total_score = 0
    with open('02/input.txt', 'r') as file:
        for line in file:
            opponent_shape = normalize_shape(line[0])
            my_shape = get_shape_based_on_round_outcome(opponent_shape, line[2])
            total_score += compute_score(opponent_shape, my_shape)
    print(f"[2] The total score with strategy #2 is {total_score}")

if __name__ == '__main__':
    main_part_one()
    main_part_two()