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

            first_compartment_set = set(line[:length//2])
            second_compartment_set = set(line[length//2:])
            sets_intersection = first_compartment_set & second_compartment_set
            priority_sum += get_priority(sets_intersection.pop()) # Assumption: exatly 1 character in common between sets
    print(f"[1] Priorities sum is {priority_sum}")

def main_part_two() -> None:
    priority_sum = 0
    with open('03/input.txt', 'r') as file:
        while True:
            set_one = set(file.readline().strip())
            set_two = set(file.readline().strip())
            set_three = set(file.readline().strip())
            if len(set_three) == 0:
                break
            sets_intersection = set_one & set_two & set_three
            priority_sum += get_priority(sets_intersection.pop())
    print(f"[2] Badges priority sum is {priority_sum}")

def get_priority(character: str) -> int:
    if 'a' <= character <= 'z':
        priority = ord(character) - ord('a') + 1  # 1 <= priority <= 26
    elif 'A' <= character <= 'Z':
        priority = ord(character) - ord('A') + 27 # 27 <= priority <= 52
    else:
        raise Exception('Unexpected character: {character}')
    return priority

if __name__ == '__main__':
    main_part_one()
    main_part_two()