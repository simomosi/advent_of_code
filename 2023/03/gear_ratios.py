'''
https://adventofcode.com/2023/day/3

Output
[1] The sum of all of the part numbers in the engine schematic is 556367
[2] The sum of gear ratios is 89471771

This script has not been OOP-ed because navigating a matrix in a smart way without allocating it is just a lot of math (+1, -1, saving positions etc).
'''

def main() -> None:
    sum = 0
    gear_ratio_sum = 0
    symbols_coordinates_set = set()
    star_simbol_pointing_adj_numbers_dict:dict[tuple[int,int], list[int]] = {} 
    with open('2023/03/input.txt', 'r') as file:
        row = 0
        for line in file:
            line = line.strip()
            for i in range(len(line)):
                c = line[i]
                if c != '.' and not c.isdigit():
                    symbols_coordinates_set.add((row, i))
                if c == '*':
                    star_simbol_pointing_adj_numbers_dict.setdefault((row,i), [])
            row += 1

        row_max = row
        file.seek(0) # reset file pointer
        row = 0
        for line in file:
            line = line.strip()
            i = 0
            while i < len(line):
                c:str = line[i]
                if c.isdigit():
                    extracted_digit = _extract_digit(line, i)
                    result = False

                    if (row, i-1) in symbols_coordinates_set: # Previous cell
                        result = True
                        _add_coordinates_to_stars_dict(star_simbol_pointing_adj_numbers_dict, extracted_digit, row, i-1)

                    if (row, i+len(extracted_digit)) in symbols_coordinates_set: # Next cell
                        result = True
                        _add_coordinates_to_stars_dict(star_simbol_pointing_adj_numbers_dict, extracted_digit, row, i+len(extracted_digit))

                    if not result and row-1 > 0: # All cells in previous row
                        perimeter_row = row-1
                        perimeter_col = i-1
                        while perimeter_col <= i+len(extracted_digit):
                            if (perimeter_row, perimeter_col) in symbols_coordinates_set:
                                result = True
                                _add_coordinates_to_stars_dict(star_simbol_pointing_adj_numbers_dict, extracted_digit, perimeter_row, perimeter_col)
                                break
                            perimeter_col += 1

                    if not result and row+1 < row_max: # All cells in next row
                        perimeter_row = row+1
                        perimeter_col = i-1
                        while perimeter_col <= i+len(extracted_digit):
                            if (perimeter_row, perimeter_col) in symbols_coordinates_set:
                                result = True
                                _add_coordinates_to_stars_dict(star_simbol_pointing_adj_numbers_dict, extracted_digit, perimeter_row, perimeter_col)
                                break
                            perimeter_col += 1

                    if result:
                        sum += int(extracted_digit)
                    i += len(extracted_digit) # skips remaining digits
                else:
                    i += 1
            row += 1

    print(f"[1] The sum of all of the part numbers in the engine schematic is {sum}")

    for numbers_list in star_simbol_pointing_adj_numbers_dict.values():
        if len(numbers_list) == 2:
            gear_ratio = int(numbers_list[0]) * int(numbers_list[1])
            gear_ratio_sum += gear_ratio

    print(f"[2] The sum of gear ratios is {gear_ratio_sum}")
            

# Extracts a digit from the matrix row starting from column i
def _extract_digit(line:str, i:int) -> str:
    pointer_end = i
    while pointer_end < len(line) and line[pointer_end].isdigit():
        pointer_end += 1
    extracted_digit = line[i:pointer_end]
    return extracted_digit

# Checks if (row,col) == '*' and adds the number in the adj list of the star sign
def _add_coordinates_to_stars_dict(star_dict:dict[tuple[int,int], list[int]], digit:str, row:int, col:int) -> bool:
    if (row, col) in star_dict:
        star_dict[(row, col)].append(digit)
        return True
    return False

if __name__ == '__main__':
    main()