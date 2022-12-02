'''
https://adventofcode.com/2022/day/1

Output
[1] Max calories owner is elf number 147 with 70613 calories
[2] The sum of calories carried by the top 3 elves is 205805

Part 1
Let n be the number of elves
Time Complexity: O(n)
Space Complexity: O(1)

Part 2
Let m be the number of the top elves to use for the computation
Time complexity: O(n)
Space complexity: O(m); after the class instantiation, this value is constant and the space complexity is O(1)
'''

class Elf:
    def __init__(self, id):
        self.id = id
        self.calories = 0

    def add_calories(self, value):
        self.calories += value

    def get_calories(self):
        return self.calories

# Saves the top m elves which brings more calories, and computes their sum
class TopElvesHandler:
    def __init__(self, max_size):
        self.elves_collection = [None] * max_size

    def add_elf(self, elf):
        if None in self.elves_collection:
            none_index = self.elves_collection.index(None)
            self.elves_collection[none_index] = elf
        else:
            min_index = self._get_min()
            if elf.get_calories() > self.elves_collection[min_index].get_calories():
                self.elves_collection[min_index] = elf
    
    def _get_min(self):
        min_index = None
        for i in range(len(self.elves_collection)):
            if min_index is None or self.elves_collection[i].get_calories() < self.elves_collection[min_index].get_calories():
                min_index = i
        return min_index

    def sum_calories(self):
        return sum(elf.get_calories() for elf in self.elves_collection)

def main():
    top_elves_handler = TopElvesHandler(3)
    max_elf = None
    current_elf = None
    elf_number = 0
    with open('input.txt', 'r') as file:
        for line in file:
            if line == '\n':
                if max_elf is None or current_elf.get_calories() > max_elf.get_calories():
                    max_elf = current_elf
                top_elves_handler.add_elf(current_elf) # Part two
                current_elf = None
                elf_number += 1
            else:
                if current_elf is None:
                    current_elf = Elf(elf_number)
                current_elf.add_calories(int(line))

    print(f"[1] Max calories owner is elf number {max_elf.id} with {max_elf.get_calories()} calories")
    print(f"[2] The sum of calories carried by the top 3 elves is {top_elves_handler.sum_calories()}")

if __name__ == '__main__':
    main()