'''
https://adventofcode.com/2022/day/11


[334, 332, 312, 301, 95, 48, 35, 21]
110888
[159983, 159957, 151092, 120006, 119996, 119970, 80006, 40003]
25590400731
'''

from collections import deque

class Monkey:
    def __init__(self, items, operation, test_divisible_by, throw_on_true, throw_on_false) -> None:
        self.items: deque[int] = items
        self.operation = operation
        self.test_divisible_by: int = test_divisible_by
        self.throw_on_true: int = throw_on_true
        self.throw_on_false: int = throw_on_false

def operation_lambda_factory(instruction: str):
    match instruction.strip().split():
        case 'old', '+', number:
            return lambda x: x+int(number)
        case 'old', '*', 'old':
            return lambda x: x**2
        case 'old', '*', number:
            return lambda x: x*int(number)
        case other:
            raise Exception('Unknown instruction:', other)

def play_monkey_game(monkeys: list[Monkey], rounds, compress = False):
    inspection_count:list[int] = [0] * len(monkeys)
    common_multiple = 1
    for m in monkeys:
        common_multiple *= m.test_divisible_by
    
    for round in range(1, rounds+1):
        for i in range(len(monkeys)):
            m = monkeys[i]
            while len(m.items) > 0:
                worry_level = m.items.popleft() % common_multiple
                inspection_count[i] += 1
                # inspect
                worry_level = m.operation(worry_level)
                # decrease worry level
                if not compress:
                    worry_level = worry_level//3
                else:
                    # worry_level %= m.test_divisible_by
                    pass
                # test and throw
                if not worry_level % m.test_divisible_by:
                    monkeys[m.throw_on_true].items.append(worry_level)
                else:
                    monkeys[m.throw_on_false].items.append(worry_level)
        # print(f"Round: {round}")
        # print(inspection_count)
    inspection_count.sort(reverse=True)
    print(inspection_count)
    print(inspection_count[0]* inspection_count[1])
    return inspection_count[0]* inspection_count[1]

def main_example_part_one():
    monkeys: list[Monkey] = []
    with open('11/input_example.txt', 'r') as file:
        while True:
            input_block = []
            for i in range(6):
                input_block.append(file.readline().strip())
            if input_block[0] == '':
                break
            
            starting_items = [int(i) for i in input_block[1].split(':')[1].split(',')]
            operation = input_block[2].split('=')[-1]
            test_divisible_by = input_block[3].split()[-1]
            throw_on_true = input_block[4].split()[-1]
            throw_on_false = input_block[5].split()[-1]
            
            operation_as_lambda = operation_lambda_factory(operation)
            m = Monkey(deque(starting_items), operation_as_lambda, int(test_divisible_by), int(throw_on_true), int(throw_on_false))
            monkeys.append(m)
            
            file.readline() # Discard
    result = play_monkey_game(monkeys, 20)
    assert result == 10605, f"Result is {result}, 10605 expected"
    
def main_part_one():
    monkeys: list[Monkey] = []
    with open('11/input.txt', 'r') as file:
        while True:
            input_block = []
            for i in range(6):
                input_block.append(file.readline().strip())
            if input_block[0] == '':
                break
            
            starting_items = [int(i) for i in input_block[1].split(':')[1].split(',')]
            operation = input_block[2].split('=')[-1]
            test_divisible_by = input_block[3].split()[-1]
            throw_on_true = input_block[4].split()[-1]
            throw_on_false = input_block[5].split()[-1]
            
            operation_as_lambda = operation_lambda_factory(operation)
            m = Monkey(deque(starting_items), operation_as_lambda, int(test_divisible_by), int(throw_on_true), int(throw_on_false))
            monkeys.append(m)
            
            file.readline() # Discard
    result = play_monkey_game(monkeys, 20) # 110888

def main_example_part_two():
    monkeys: list[Monkey] = []
    with open('11/input_example.txt', 'r') as file:
        while True:
            input_block = []
            for n in range(6):
                input_block.append(file.readline().strip())
            if input_block[0] == '':
                break
            
            starting_items = [int(i) for i in input_block[1].split(':')[1].split(',')]
            operation = input_block[2].split('=')[-1]
            test_divisible_by = input_block[3].split()[-1]
            throw_on_true = input_block[4].split()[-1]
            throw_on_false = input_block[5].split()[-1]
            
            operation_as_lambda = operation_lambda_factory(operation)
            m = Monkey(deque(starting_items), operation_as_lambda, int(test_divisible_by), int(throw_on_true), int(throw_on_false))
            monkeys.append(m)
            
            file.readline() # Discard
    result = play_monkey_game(monkeys, 10000, True) # 32397480045 Too high

def main_part_two():
    monkeys: list[Monkey] = []
    with open('11/input.txt', 'r') as file:
        while True:
            input_block = []
            for i in range(6):
                input_block.append(file.readline().strip())
            if input_block[0] == '':
                break
            
            starting_items = [int(i) for i in input_block[1].split(':')[1].split(',')]
            operation = input_block[2].split('=')[-1]
            test_divisible_by = input_block[3].split()[-1]
            throw_on_true = input_block[4].split()[-1]
            throw_on_false = input_block[5].split()[-1]
            
            operation_as_lambda = operation_lambda_factory(operation)
            m = Monkey(deque(starting_items), operation_as_lambda, int(test_divisible_by), int(throw_on_true), int(throw_on_false))

            monkeys.append(m)
            
            file.readline() # Discard
    result = play_monkey_game(monkeys, 10000, True)

if __name__ == '__main__':
    #main_example_part_one()
    main_part_one()
    #main_example_part_two()
    main_part_two()
