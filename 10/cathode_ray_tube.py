'''
https://adventofcode.com/2022/day/10
Output

###..####.####.####.#..#.###..####..##..
#..#.#.......#.#....#.#..#..#.#....#..#.
#..#.###....#..###..##...###..###..#..#.
###..#.....#...#....#.#..#..#.#....####.
#.#..#....#....#....#.#..#..#.#....#..#.
#..#.#....####.####.#..#.###..#....#..#.

[1] Sum of the signal strength is 15220

Let n be the number of instructions

Time Complexity: O(n)
Space Complexity: O(1) because the queue is consumed after reading every instruction, it holds at most 2 instructions. Printing pixels does not occupy memory
'''

from collections import deque

def main_mock():
    with open('10/input_mock_1.txt', 'r') as file:
        signal_strength = compute_signal_strength(file)
    print()
    assert signal_strength == 13_140, f"Signal strength should be 13140, actual is {signal_strength}"

def main():
    with open('10/input.txt', 'r') as file:
        signal_strength = compute_signal_strength(file)
    print(f"\n[1] Sum of the signal strength is", signal_strength)

def compute_signal_strength(file):
    register: int = 1
    cycle: int = 0
    signal_strength: int = 0
    add_queue: deque[int] = deque()
    for line in file: #['noop', 'addx 3', 'addx -5']:
        match line.strip().split():
            case ['noop']:
                add_queue.append(0)
            case ['addx', number]:
                add_queue.append(0)
                add_queue.append(int(number))
            case other:
                raise Exception("Unknown instruction: ", other)
        while len(add_queue) > 0:
            cycle += 1
            # Cycle start
            if not (cycle-20)%40:
                signal_strength += cycle * register
            draw_crt(cycle, register)
            # Cycle end
            register += add_queue.popleft()
    return signal_strength

def draw_crt(cycle: int, sprite_position: int):
    current_pixel = (cycle-1)%40
    if sprite_position -1 <= current_pixel <= sprite_position +1:
        print('#', end='')
    else:
        print('.', end='')
    if not cycle%40:
        print()

if __name__ == '__main__':
    main_mock()
    main()
    
    
