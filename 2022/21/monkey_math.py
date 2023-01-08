'''
https://adventofcode.com/2022/day/21

Output:
[1] The monkey named root will yell number 379578518396784
[2] The number to pass root's equality test is 3353687996514
'''

import re
from typing import NamedTuple, Callable
from enum import Enum

class MonkeyType(Enum):
    YELL=0,
    MATH=1

job_yell_re = re.compile('(\w+): (\d+)') # btrn: 10
job_math_re = re.compile('(\w+): (\w+) (\+|\-|\*|\/) (\w+)') # root: vtsj + tfjf

class Monkey:
    def __init__(self, name:str, type:MonkeyType):
        self.name = name
        self.type = type
        
    def job(self):
        raise Exception("Method Monkey.job() must be implemented")
    
    def get_dependencies(self) -> list[str]:
        return []
        
class MonkeyYell(Monkey):
    def __init__(self, name:str, value:int):
        super().__init__(name, MonkeyType.YELL)
        self.value = value
        
    def job(self):
        return self.value
        
class MonkeyMath(Monkey):
    def __init__(self, name:str, monkey_left:str, operator:str, monkey_right:str):
        super().__init__(name, MonkeyType.MATH)
        self.monkey_left = monkey_left
        self.operator = operator
        self.monkey_right = monkey_right
        
    def job(self, left:int, right: int):
        match self.operator:
            case '+':
                return left+right
            case '-':
                return left-right
            case '*':
                return left*right
            case '/':
                return left//right
            case other:
                raise Exception('Unknown operator:', other)
            
    def get_dependencies(self) -> list[str]:
        return [self.monkey_left, self.monkey_right]

def example():
    monkeys=read_input('21/example.txt')
    result = solve_riddle(monkeys)
    assert result == 152, f"Expected 152, actual {result}"
    result = solve_real_riddle(monkeys)

def main():
    monkeys=read_input('21/input.txt')
    result = solve_riddle(monkeys)
    print(f"[1] The monkey named root will yell number {result}")
    result = solve_real_riddle(monkeys)
    print(f"[2] The number to pass root's equality test is {result}")
      
def read_input(filename:str) -> dict[str, Monkey]:
    monkeys:dict[str, Monkey] = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if match_yell_monkey:= job_yell_re.match(line):
                name, number = match_yell_monkey.groups()
                m = MonkeyYell(name, int(number))
                monkeys.setdefault(name, m)
            elif match_math_monkey := job_math_re.match(line):
                name, monkey_left, operand, monkey_right = match_math_monkey.groups()
                m = MonkeyMath(name, monkey_left, operand, monkey_right)
                monkeys.setdefault(name, m)
            else:
                raise Exception('Unexpected input:', line)
    return monkeys
            
def solve_riddle(monkeys:dict[str, Monkey]) -> int :
    cache:dict[str, int] = {}
    name = 'root'
    return _solve_yell(monkeys, name, cache)
    
def _solve_yell(monkeys: dict[str, Monkey], name:str, cache:dict[str, int]) -> int :
    if name in cache:
        return cache.get(name)
    m = monkeys.get(name)
    if m.type == MonkeyType.YELL:
        result = m.job()
    else:
        result_collection:list[int] = []
        for other_monkey_name in m.get_dependencies():
            result_collection.append(_solve_yell(monkeys, other_monkey_name, cache))
        result = m.job(*result_collection)
    cache.setdefault(name, result)
    return result

def solve_real_riddle(monkeys:dict[str, Monkey]) -> str:
    root_name = 'root'
    target_name = 'humn'
    
    root_monkey = monkeys.get(root_name)
    root_left, root_right = root_monkey.get_dependencies()
    equality_value = _solve_yell(monkeys, root_right, {})
    
    independent_values_from_humn:dict[str, int] = {}
    _get_independent_values_from_hman(monkeys, root_name, target_name, independent_values_from_humn)
    independent_values_from_humn = {k:v for k,v in independent_values_from_humn.items() if not v is None}
    
    path_to_humn:list[Monkey] = []
    found = _find_path_to_hman(monkeys, root_name, target_name, path_to_humn)
    
    result = _get_hman_value_for_equality(equality_value, independent_values_from_humn, path_to_humn)
    return result

def _find_path_to_hman(monkeys: dict[str, Monkey], name:str, target_name:str, path:list[Monkey]) -> bool:
    m = monkeys.get(name)
    path.append(m)
    if name == target_name:
        return True
    for adj in m.get_dependencies():
        result = _find_path_to_hman(monkeys, adj, target_name, path)
        if result:
            return True
    path.pop()
    return False
            

def _get_independent_values_from_hman(monkeys: dict[str, Monkey], name:str, target_name:str, cache:dict[str, int]) -> int:
    if name in cache:
        return cache.get(name)
    m = monkeys.get(name)
    if m.name == target_name:
        return None
    if m.type == MonkeyType.YELL:
        result = m.job()
    else:
        monkey_left, monkey_right = m.get_dependencies()
        result_left = _get_independent_values_from_hman(monkeys, monkey_left, target_name, cache)
        result_right = _get_independent_values_from_hman(monkeys, monkey_right, target_name, cache)
        result = None if not result_left or not result_right else m.job(result_left, result_right)
    cache.setdefault(name, result)
    return result

def _get_hman_value_for_equality(equality_value:int, independent_values_from_humn:dict[str, int], path_to_humn:list[Monkey]) -> int:
    path_to_humn.reverse()
    while path_to_humn:
        m = path_to_humn.pop()
        if m.name == 'root' or m.name == 'humn':
            continue
        left_monkey, right_monkey = m.get_dependencies()
        left_result = independent_values_from_humn.get(left_monkey, None)
        right_result = independent_values_from_humn.get(right_monkey, None)
        if right_result and not left_result: # e.g. x + 3 = 150 => x = 150-3
            equality_value = _compute_opposite_operator_result(m.operator, equality_value, right_result)
        elif left_result and not right_result: # e.g. 3 - x = 150 => x = -150+3
            if m.operator == '-': # 2 - x = 100 => x = 2-100 = -(100-2)
                equality_value = _compute_opposite_operator_result(m.operator, equality_value, - left_result)
                equality_value *= -1
            elif m.operator == '/': # 2/x = 100 => x = 2/100 = 100^-1 * 2
                equality_value = _compute_opposite_operator_result(m.operator, equality_value**-1, left_result)
            else:
                equality_value = _compute_opposite_operator_result(m.operator, equality_value, left_result)
        else:
            raise Exception('Unexpected case')
    return equality_value

def _compute_opposite_operator_result(operator:str, left:int, right: int) -> int:
    match operator:
        case '+':
            return left-right
        case '-':
            return left+right
        case '*':
            return left//right
        case '/':
            return left*right
        case other:
            raise Exception('Unknown operator:', other)
            
if __name__ == '__main__':
    example()
    main()