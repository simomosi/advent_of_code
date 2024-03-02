'''
https://adventofcode.com/2023/day/2

Output
[1] The sum of the IDs of those games is 2679
[2] The sum of powers of these games is 77607

Part 1 and 2
Let n be the number of games
Let s be the biggest set number in a game
Let c be the number of colors in the game

Time Complexity is O(n*c*s) for input parsing and iterating colors(*)
Space Complexity is O(c*s) for storing colors and values (just one game at a time)

(*) The time complexity of a single color check is constant thanks to dictionaries, but this would have masked the real problem complexity
'''

import re

def main() -> None:
    input_parser = InputParser()
    games_checker = GamesChecker(12, 13, 14)
    total = 0
    powers_sum = 0
    with open('2023/02/input.txt', 'r') as file:
        for line in file:
            id, gameset_dictionary_list = input_parser.parse(line)

            # Part 1
            if games_checker.check_all_gamesets(gameset_dictionary_list):
                total += int(id)
            # Part 2
                
            max_number_of_color_cubes_dictionary = games_checker.retrieve_max_number_of_each_color(gameset_dictionary_list)
            power = max_number_of_color_cubes_dictionary.get("red") * max_number_of_color_cubes_dictionary.get("green") * max_number_of_color_cubes_dictionary.get("blue")
            powers_sum += power
    print(f"[1] The sum of the IDs of those games is {total}")
    print(f"[2] The sum of powers of these games is {powers_sum}")

# Class to parse the input in the form of "Game 1: 7 red, 8 blue; 6 blue, 6 red, 2 green; ..."
class InputParser():
    def __init__(self):
        self.line_regex = re.compile('Game (\d+): (.*)$')
        self.gameset_regex = re.compile('(\d+) (red|green|blue)')

    # Parse the whole line
    def parse(self, line:str) -> tuple[int, list[dict[str,int]]]:
        line_regex_result = self.line_regex.search(line.strip())
        id, rest_of_string = line_regex_result.groups()
        gameset_dictionary_list = self._extract_gameset_dictionary_list(rest_of_string)
        
        return id, gameset_dictionary_list
    
    # Parse from '7 red, 8 blue; 6 blue, 6 red, 2 green' to [{"red": 7, "green": 0, "blue": 8}, {"red": 6, "green": 2, "blue": 6}]
    def _extract_gameset_dictionary_list(self, whole_game:str) -> list[dict[str, int]]:
            gameset_collection = []
            for gameset in whole_game.split(";"):
                gameset_dictionary = self._extract_gameset_dictionary(gameset)
                gameset_collection.append(gameset_dictionary)
            return gameset_collection
    
    # Parse from '7 red, 8 blue' to {"red": 7, "green": 0, "blue": 8}
    def _extract_gameset_dictionary(self, gameset:str) -> dict[str, int]:
        gameset_dictionary = {"red": 0, "green": 0, "blue": 0}

        gameset_regex_result = self.gameset_regex.findall(gameset)
        for number, color in gameset_regex_result:
            gameset_dictionary[color] = int(number)

        return gameset_dictionary

# Class which checks if game costraints are respected
class GamesChecker():
    def __init__(self, max_red:int, max_green:int, max_blue:int):
        self.max_red = max_red
        self.max_green = max_green
        self.max_blue = max_blue

    # Checks if constraints of every game sets are respected
    def check_all_gamesets(self, gameset_dictionary_list: list[dict[str, int]]) -> bool:
        for gameset_dictionary in gameset_dictionary_list:
            if (not self.check_single_gameset(gameset_dictionary)):
                return False
        return True

    # Checks if constraints of a single game set are respected
    def check_single_gameset(self, gameset_dictionary: dict[str, int]) -> bool:
        return gameset_dictionary.get("red", 0) <= self.max_red  and \
            gameset_dictionary.get("green", 0) <= self.max_green and \
            gameset_dictionary.get("blue", 0) <= self.max_blue \
            
    # Retrieve the minimum number of colors to make the game valid, in the form of a dictionary
    def retrieve_max_number_of_each_color(self, gameset_dictionary_list: list[dict[str, int]]) -> dict[str, int]:
        max_number_gameset_dictionary = {"red": 0, "green": 0, "blue": 0}
        for gameset_dictionary in gameset_dictionary_list:
            for color, number in gameset_dictionary.items():
                previous_number = max_number_gameset_dictionary[color]
                max_number_gameset_dictionary[color] = max(previous_number, number)
        return max_number_gameset_dictionary

if __name__ == '__main__':
    main()