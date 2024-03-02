'''
https://adventofcode.com/2023/day/1

Output
[1] The sum of all calibration values is 54951
[2] The sum of all calibration values is 55218

Part 1
Let n be the number of strings
Let c be the biggest string

Time Complexity is O(n*c)
Space Complexity is O(1)

Part 2
Let k be the number of digits names we are checking. Right now k=9.

Time Complexity is O(n*c*k); it can be lowered to O(n*c) using a Trie to store digit names.
Space Complexity is O(1)
'''

def main_part_one() -> None:
    calibration_values_sum = 0
    digits_extractor = DigitsExtractor()
    with open('2023/01/input.txt', 'r') as file:
        for line in file:
            calibration_value = digits_extractor.find_digits(line.strip())
            calibration_values_sum += calibration_value
    print(f"[1] The sum of all calibration values is {calibration_values_sum}")

def main_part_two() -> None:
    calibration_values_sum = 0
    digits_extractor = DigitsAndNamesExtractor()
    with open('2023/01/input.txt', 'r') as file:
        for line in file:
            calibration_value = digits_extractor.find_digits(line.strip())
            calibration_values_sum += calibration_value
    print(f"[2] The sum of all calibration values is {calibration_values_sum}")


class DigitsExtractor():
    def __init__(self):
        pass

    # Extracts and combine first and last digit in a string
    def find_digits(self, line: str) -> int:
        first = last = None
        for c in line:
            if c.isdigit():
                first = c
                break
        for c in line[::-1]:
            if c.isdigit():
                last = c
                break
        return int(first + last)
    
class DigitsAndNamesExtractor(DigitsExtractor):
    def __init__(self):
        super().__init__()

        self.name_digits_dict = {
            #"zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9"
        }

    # Extracts and combine first and last digit in a string
    def find_digits(self, line: str) -> int:
        first_digit = second_digit = None
        for i in range(len(line)):
            if line[i].isdigit():
                #digits.append(line[i])
                if not first_digit:
                    first_digit = line[i]
                else:
                    second_digit = line[i]
            else:
                for key, value in self.name_digits_dict.items():
                    if line[i:].startswith(key):
                        if not first_digit:
                            first_digit = value
                        else:
                            second_digit = value
                        break
        if not second_digit:
            second_digit = first_digit
        result = first_digit + second_digit
        return int(result)

if __name__ == '__main__':
    main_part_one()
    main_part_two()