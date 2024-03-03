'''
https://adventofcode.com/2023/day/4

Output
[1] Points worth in total are 27845
[2] Total number of copies is 9496801

Part 1
Let n be the number of scratchcards
Let u be the number of "user numbers"

Time Complexity: O(n*u)
Space Complexity: O(1) -> actually I use an array of user winning numbers, but it's just for syntactic sugar! It can be done with a for loop.

Part 2
Let w be the number of "winning numbers"

Time Complexity: O(n*w)
Space Complexity: O(n) to store an entry for each ID
'''

import re

def main() -> None:
    game_handler = GameHandler()
    input_parser = InputParser()
    points_total = 0
    with open('2023/04/input.txt', 'r') as file:
        for line in file:
            id, winning_numbers, user_numbers = input_parser.parse(line.strip())
            game_handler.register_game(id)
            score = game_handler.compute_score(id, winning_numbers, user_numbers)
            points_total += score

    total_number_of_copies = game_handler.get_number_of_copies()
    print(f"[1] Points worth in total are {points_total}")
    print(f"[2] Total number of copies is {total_number_of_copies}")

class InputParser:
    def __init__(self):
        self.line_regex = re.compile('^Card \s*(\d+): ([\s\d]+) \| ([\s\d]+)$')

    def parse(self, line:str) -> tuple[int, set[int], list[int]]:
        regex_result = self.line_regex.match(line)
        card_number, winning_string, my_numbers_string = regex_result.groups()

        winning_numbers_list = set(map(int, winning_string.split()))
        user_numbers = map(int, my_numbers_string.split())
        return int(card_number), winning_numbers_list, user_numbers

class GameHandler:
    def __init__(self):
        self.number_of_copies_dict: dict[int, int] = {1:1}

    # Register the first scratchcard of a game if it has not been encountered before
    def register_game(self, id:int) -> None:
        if id not in self.number_of_copies_dict:
            self.number_of_copies_dict[id] = 1

    def compute_score(self, id:int, winning_numbers:set[int], user_numbers:list[int]) -> int:
        hits = 0
        hits = len([n for n in user_numbers if n in winning_numbers])
        self._register_hits(id, hits)
        return 2**(hits-1) if hits > 0 else 0

    def _register_hits(self, id:int, hits:int) -> None:
        base_number = self.number_of_copies_dict.get(id, 1)
        for i in range(1, hits+1):
            target_number = self.number_of_copies_dict.get(id+i, 1)
            target_number += base_number
            self.number_of_copies_dict[id+i] = target_number

    def get_number_of_copies(self) -> int:
        return sum(self.number_of_copies_dict.values())


if __name__ == '__main__':
    main()