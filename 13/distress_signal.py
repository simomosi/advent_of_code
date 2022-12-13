'''
https://adventofcode.com/2022/day/13

Output
[1] Sum of correct indices is 6046
'''

import functools

def example_part_one():
    packages_couples_list = []
    with open('13/example_input.txt', 'r') as file:
        while True:
            line_one = file.readline().strip()
            line_two = file.readline().strip()
            file.readline()
            
            if line_one == '' or line_two == '':
                break
            packet_one, _ = parse_input_line(line_one)
            packet_two, _ = parse_input_line(line_two)

            packages_couples_list.append((packet_one, packet_two))
    sum_of_correct_indices = sum(i for i, p in enumerate(packages_couples_list, start=1) if are_ordered(p[0], p[1]))
    assert sum_of_correct_indices == 13, f"Expected 13, actual {sum_of_correct_indices}"

def main_part_one():
    packages_couples_list = []
    with open('13/input.txt', 'r') as file:
        while True:
            line_one = file.readline().strip()
            line_two = file.readline().strip()
            file.readline()
            
            if line_one == '' or line_two == '':
                break
            packet_one, _ = parse_input_line(line_one)
            packet_two, _ = parse_input_line(line_two)
            
            packages_couples_list.append((packet_one, packet_two))
    sum_of_correct_indices = sum(i for i, p in enumerate(packages_couples_list, start=1) if are_ordered(p[0], p[1]))
    print(f"[1] Sum of correct indices is", sum_of_correct_indices)
    
def example_part_two():
    packages_list = []
    with open('13/example_input.txt', 'r') as file:
        for line in file:
            if line.strip() == '':
                continue
            packet, _ = parse_input_line(line)
            packages_list.append(packet)
            
    divider_packet_one, _ = parse_input_line('[[2]]')
    packages_list.append(divider_packet_one)
    divider_packet_two, _ = parse_input_line('[[6]]')
    packages_list.append(divider_packet_two)
    
    ordered_list = sorted(packages_list, key= functools.cmp_to_key(lambda left,right: -1 if are_ordered(left, right) else 1))
    index_one = ordered_list.index([[2]]) + 1
    index_two = ordered_list.index([[6]]) + 1
    index_multiplication = index_one * index_two
    assert index_multiplication == 140, f"Expected 140, actual {index_multiplication}"
    
def main_part_two():
    packages_list = []
    with open('13/input.txt', 'r') as file:
        for line in file:
            if line.strip() == '':
                continue
            packet, _ = parse_input_line(line)
            packages_list.append(packet)
            
    divider_packet_one, _ = parse_input_line('[[2]]')
    packages_list.append(divider_packet_one)
    divider_packet_two, _ = parse_input_line('[[6]]')
    packages_list.append(divider_packet_two)
    
    ordered_list = sorted(packages_list, key= functools.cmp_to_key(lambda left,right: -1 if are_ordered(left, right) else 1))
    index_one = ordered_list.index([[2]]) + 1
    index_two = ordered_list.index([[6]]) + 1
    index_multiplication = index_one * index_two
    print(f"[2] Multiplication of divider packets indices is", index_multiplication)
            
    
def parse_input_line(line: str, start_position: int = 0) -> tuple[list, int]:
    data: list = []
    digits_buffer: str = ''
    assert line[start_position] == '[', f"Error: expected an opened bracket as start position, '{line[start_position]}' actual"

    current_position = start_position + 1
    while True:
        match line[current_position]:
            case '[':
                sub_data, current_position = parse_input_line(line, current_position)
                data.append(sub_data)
            case ']':
                break
            case ',':
                pass
            case _:
                digits_buffer = line[current_position]
                while line[current_position+1].isdecimal():
                    digits_buffer += line[current_position+1]
                    current_position += 1
                data.append(int(digits_buffer))
                digits_buffer = ''
        current_position += 1
    return (data, current_position)
            
def are_ordered(package_left: list, package_right: list) -> bool:
    for p1, p2 in zip(package_left, package_right):
        result = compare(p1, p2)
        if result is not None:
            return result
    if len(package_left) < len(package_right):
        return True
    if len(package_left) > len(package_right):
        return False
        
def compare(data_left: int|list, data_right: int|list) -> bool:
    if type(data_left) is int and type(data_right) is int:
        if data_left < data_right:
            return True
        if data_left > data_right:
            return False
    elif type(data_left) is list and type(data_right) is list:
        for left, right in zip(data_left, data_right):
            result = compare(left, right)
            if result is not None:
                return result
        if len(data_left) < len(data_right):
            return True
        if len(data_left) > len(data_right):
            return False
    else:
        casted_data_left = data_left
        casted_data_right = data_right
        if type(data_left) is int:
            casted_data_left = list([data_left])
        if type(data_right) is int:
            casted_data_right = list([data_right])
        result = compare(casted_data_left, casted_data_right)
        if result is not None:
            return result
    return None
             
if __name__ == '__main__':
    example_part_one()
    main_part_one()
    example_part_two()
    main_part_two()