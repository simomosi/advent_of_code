'''
https://adventofcode.com/2022/day/25

Output
[1] The SNAFU number to supply in the console is 2-00=12=21-0=01--000
'''

digit_map = {
    '-': -1,
    '=': -2,
    '0': 0,
    '1': 1,
    '2': 2
}

def example():
    snafu_list = _read_input('25/example.txt')
    snafu_sum = sum(decode_snafu(s) for s in snafu_list)
    assert snafu_sum == 4890, f"Expected 4890, actual {snafu_sum}"
    result = encode_snafu(snafu_sum)
    assert result == '2=-1=0', f"Expected '2=-1=0', actual {result}"

def main():
    snafu_list = _read_input('25/input.txt')
    snafu_sum = sum(decode_snafu(s) for s in snafu_list)
    result = encode_snafu(snafu_sum)
    print(f"[1] The SNAFU number to supply in the console is {result}") # Wrong 2=-1=0

def _read_input(filename):
    snafu_list:list[str] = []
    with open(filename, 'r') as file:
        for line in file:
            snafu_list.append(line.strip())
    return snafu_list

def decode_snafu(encoded_number:str) -> int:
    total = 0
    length = len(encoded_number)
    for position in range(length):
        digit = encoded_number[length-position-1]
        decodeddigit = digit_map.get(digit)
        total += decodeddigit * (5**position)
    return total
            
def encode_snafu(decimal_number:int) -> str:
    q = decimal_number
    r = 0
    result = ''
    while q > 0:
        r = q % 5
        q //= 5
        # Increment the next power by 1 unit, then "subtract" -2 (3 = 5-2) or -1 (4 = 5-1)
        # e.g. 4/5 -> q=0 r=4 but also q = 1 r = 5-1 = -1 = character "-"
        if r > 2:
            q += 1 
            if r == 3:
                result += '='
            elif r == 4:
                result += '-'
        else:
            result += str(r)
    return result[::-1]

if __name__ == '__main__':
    example()
    main()

