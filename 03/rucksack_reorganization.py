'''
https://adventofcode.com/2022/day/3

Part 1 and 2
Let m be the length of the longest string
Let n be the number of lines in the input file
Time Complexity:
- Read through n lines
- Split each line in half (each of m/2 characters)
- Put each half in a Set (O(m/2) time) and compute sets intersection (O(m/2) time if Python does it in the best way)
Total complexity is O(n*m)
Space Complexity: O(m)

Output
[1] Priorities sum is 7428
[2] Badges priority sum is 2650
'''

def main_part_one() -> None:
    priority_sum = 0
    with open('03/input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            length = len(line)
            first_compartment = line[:length//2]
            second_compartment = line[length//2:]

            first_compartment_set = {c for c in first_compartment}
            second_compartment_set = {c for c in second_compartment}
            set_intersection = first_compartment_set & second_compartment_set
            priority_sum += get_priority(set_intersection.pop())
            
    print(f"[1] Priorities sum is {priority_sum}")

def main_part_two() -> None:
    priority_sum = 0
    with open('03/input.txt', 'r') as file:
        while True:
            rucksack_one = file.readline().strip()
            rucksack_two = file.readline().strip()
            rucksack_three = file.readline().strip()
            if rucksack_one == '':
                break

            set_one = {c for c in rucksack_one}
            set_two = {c for c in rucksack_two}
            set_three = {c for c in rucksack_three}
            set_intersection = set_one & set_two & set_three
            priority_sum += get_priority(set_intersection.pop())
    print(f"[2] Badges priority sum is {priority_sum}")

def get_priority(character: str) -> int:
    if 'a' <= character <= 'z':
        priority = ord(character)-96 # 1 <= priority <= 26
    elif 'A' <= character <= 'Z':
        priority = ord(character) - ord('A') + 27 # 27 <= priority <= 52
    else:
        raise Exception('Unexpected character: {character}')
    return priority

if __name__ == '__main__':
    main_part_one()
    main_part_two()