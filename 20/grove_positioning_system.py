'''
https://adventofcode.com/2022/day/20

Output
[1] The sum of the three numbers that form the grove coordinates is 11037
[2] The sum of the three decrypted numbers that form the grove coordinates is 3033720253914
'''

from collections import deque

def example():
    linked_list:list[tuple[int,int]] = []
    index = 0
    with open('20/example.txt', 'r') as file:
        for line in file:
            value = int(line.strip())
            if value in linked_list:
                print(f"Value {value} already found at position {linked_list.index(value)}")
            linked_list.append((value, index))
            index += 1
    result, _ = mixing(linked_list)
    assert result == 3, f"Expected 3, actual {result}"
    result, _ = mixing_with_encryption(linked_list, 811589153, 10)
    assert result == 1623178306, f"Expected 1623178306, actual {result}"

def main():
    linked_list:list[tuple[int,int]] = []
    index = 0
    with open('20/input.txt', 'r') as file:
        for line in file:
            value = int(line.strip())
            if value in linked_list:
                print(f"Value {value} already found at position {linked_list.index(value)}")
            linked_list.append((value, index))
            index += 1
    result, _ = mixing(linked_list)
    print(f"[1] The sum of the three numbers that form the grove coordinates is {result}")
    result, _ = mixing_with_encryption(linked_list, 811589153, 10)
    print(f"[2] The sum of the three decrypted numbers that form the grove coordinates is {result}")

def mixing(original_list:list[tuple[int,int]]) -> tuple[int, deque[tuple[int,int]]]:
    size = len(original_list)
    sorting_list:deque[tuple[int,int]] = deque()
    for v, i in original_list:
        sorting_list.append((v,i))
    
    _do_mix(original_list, sorting_list)
    _make_list_start_at_zero(sorting_list)

    result = sum([sorting_list[i%size][0] for i in (1000,2000,3000)])
    return result, sorting_list

def mixing_with_encryption(original_list:list[tuple[int,int]], decryption_key:int, times:int) -> int:
    size = len(original_list)
    decrypted_list = [(v*decryption_key,i) for v, i in original_list]
    sorting_list:deque[tuple[int,int]] = deque()
    for v, i in decrypted_list:
        sorting_list.append((v,i))
    
    while times > 0:
        _do_mix(decrypted_list, sorting_list)
        times -= 1
        
    _make_list_start_at_zero(sorting_list)
    result = sum([sorting_list[i%size][0] for i in (1000,2000,3000)])
    return result, sorting_list

def _do_mix(original_list:list[tuple[int,int]], sorting_list:deque[tuple[int,int]]) -> None:
    size = len(original_list)
    for i in range(size):
        value, index = original_list[i]
        while sorting_list[0] != (value, index):
            _shiftBackward(sorting_list, 1)
        head = sorting_list.popleft() # size becomes size-1
        if value >= 0:
            _shiftBackward(sorting_list, value%(size-1))
        else:
            _shiftForward(sorting_list, -value%(size-1))
        sorting_list.appendleft(head)
    return

def _shiftForward(list: deque[tuple[int,int]], steps:int) -> None:
    while steps > 0:
        tmp = list.pop()
        list.appendleft(tmp)
        steps -= 1
        
def _shiftBackward(list: deque[tuple[int,int]], steps:int) -> None:
    while steps > 0:
        tmp = list.popleft()
        list.append(tmp)
        steps -= 1
        
def _make_list_start_at_zero(list: deque[tuple[int,int]]) -> None:
    while True:
        value, _ = list[0]
        if value == 0:
            break
        _shiftBackward(list, 1)
    return

if __name__ == '__main__':
    example()
    main()