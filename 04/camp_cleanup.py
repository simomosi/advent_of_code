'''
https://adventofcode.com/2022/day/3

Output
[1] Number of ranges which fully contains the other: 413
[2] Number of ranges intersections: 806

Time Complexity: O(n)
Space Complexity: O(1)
'''

class Section:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

def main():
    number_of_ranges_which_fully_contains_the_other = 0
    number_of_intersections = 0
    with open('04/input.txt', 'r') as file:
        for line in file:
            range_one, range_two = line.strip().split(',')
            start_one, end_one = map(int, range_one.split('-'))
            start_two, end_two = map(int, range_two.split('-'))
            s1 = Section(start_one, end_one)
            s2 = Section(start_two, end_two)

            if  section_contains_the_other(s1, s2):
                number_of_ranges_which_fully_contains_the_other += 1
            if section_overlaps_the_other(s1, s2):
                number_of_intersections += 1

    print(f"[1] Number of ranges which fully contains the other: {number_of_ranges_which_fully_contains_the_other}")
    print(f"[2] Number of ranges intersections: {number_of_intersections}")

def section_contains_the_other(first: Section, second: Section) -> bool :
    return first.start <= second.start <= second.end <= first.end or \
        second.start <= first.start <= first.end <= second.end

def section_overlaps_the_other(first: Section, second: Section) -> bool:
    return  first.start <= second.start <= first.end <= second.end or \
            second.start <= first.start <= second.end <= first.end or \
            section_contains_the_other(first, second)

if __name__ == '__main__':
    main()
