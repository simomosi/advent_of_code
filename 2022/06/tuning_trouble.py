'''
https://adventofcode.com/2022/day/6

Output
[1] Packet marker <hfvd> occurs after 1142 characters
[2] Message marker <tnfsdzpvcgbjqw> occurs after 2803 characters

Let n be the number of characters
Let p be the packet length
Let m be the message length

Time Complexity:
- For each character in input (O(n))
- Decrease old character occurrences (O(1) assuming dict.update method is well implemented)
- Increase new character occurrences (O(1) assuming dict.update method is well implemented)
- Update marker (O(1) thanks to collections.deque)
Total: O(n)

Space Complexity:
O(p) for part 1, O(m) for part 2
Dictionary size is O(size_of_the_alphabet)
'''

from collections import deque

class SlidingWindow:
    def __init__(self, initial_string: str):
        self.characters_occurrence_map: dict[str, int] = {}
        self.characters_added: int = len(initial_string)
        self.marker: deque = deque(maxlen=self.characters_added)
        for c in initial_string:
            self.marker.append(c)
            occurrences = self.characters_occurrence_map.get(c, 0)
            self.characters_occurrence_map.update({c: occurrences+1})
            
    def slide(self, new_character: str) -> None:
        old_character = self.marker.popleft()
        old_character_occurrences = self.characters_occurrence_map.get(old_character)
        self.characters_occurrence_map.update({old_character: old_character_occurrences-1})

        new_character_occurrences = self.characters_occurrence_map.get(new_character, 0)
        self.characters_occurrence_map.update({new_character: new_character_occurrences+1})

        self.characters_added += 1
        self.marker.append(new_character)

    def is_valid_marker(self) -> bool:
        for c in self.marker:
            if self.characters_occurrence_map.get(c) > 1:
                return False
        return True

    def get_marker(self) -> str:
        return "".join(self.marker)

def main_part_one():
    with open('06/input.txt', 'r') as file:
        sliding_window = SlidingWindow(file.read(4))
        while not sliding_window.is_valid_marker():
            char = file.read(1)
            if char == '':
                raise Exception('EOF reached')
            sliding_window.slide(char)
    print(f"[1] Packet marker <{sliding_window.get_marker()}> occurs after {sliding_window.characters_added} characters")

def main_part_two():
    with open('06/input.txt', 'r') as file:
        sliding_window = SlidingWindow(file.read(14))
        while not sliding_window.is_valid_marker():
            char = file.read(1)
            if char == '':
                raise Exception('EOF reached')
            sliding_window.slide(char)
    print(f"[2] Message marker <{sliding_window.get_marker()}> occurs after {sliding_window.characters_added} characters")


if __name__ == '__main__':
    main_part_one()
    main_part_two()