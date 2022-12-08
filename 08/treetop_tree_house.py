'''
https://adventofcode.com/2022/day/8

Output
[1] The number of trees visible from outside the grid is 1736
[2] The highest scenic score is 268800
'''

def main():
    grid: list[list[int]] = []
    with open('08/input.txt', 'r') as file:
        for line in file:
            grid.append(list(map(int, line.strip())))

    rows = len(grid)
    columns = len(grid[0])
    visible_number:int = 0
    scenic_scores:list[int] = []
    for i in range(rows):
        for j in range(columns):
            visible_number += is_visible(grid, i, j, rows, columns)
            scenic_scores.append(compute_scenic_score(grid, i, j, rows, columns))
    
    print(f"[1] The number of trees visible from outside the grid is {visible_number}")
    print(f"[2] The highest scenic score is {max(scenic_scores)}") # 124 too low

def is_visible(grid: list[list[int]], row_index: int, column_index: int, rows_number: int, columns_number: int) -> bool:
    if row_index == 0 or row_index == rows_number-1:
        return True
    if column_index == 0 or column_index == columns_number-1:
        return True
    
    height: int = grid[row_index][column_index]

    max_height_row_left = max(grid[i][column_index] for i in range(row_index))
    max_height_row_right = max(grid[i][column_index] for i in range(row_index+1, rows_number))
    max_height_col_up = max(grid[row_index][j] for j in range(column_index))
    max_height_col_down = max(grid[row_index][j] for j in range(column_index+1, columns_number))
    # Benchmark can be improved using short-circuit evaluation
    return (height > max_height_row_left or
            height > max_height_row_right or
            height > max_height_col_up or
            height > max_height_col_down)

def compute_scenic_score(grid: list[list[int]], row_index: int, column_index: int, rows_number: int, columns_number: int) -> int:
    if row_index == 0 or row_index == rows_number-1:
        return 0
    if column_index == 0 or column_index == columns_number-1:
        return 0
    height: int = grid[row_index][column_index]

    score_up: int = 0
    for i in range(row_index-1, -1, -1):
        score_up += 1
        if grid[i][column_index] >= height:
            break

    score_down: int = 0
    for i in range(row_index+1, rows_number):
        score_down += 1
        if grid[i][column_index] >= height:
            break

    score_left: int = 0
    for j in range(column_index-1, -1, -1):
        score_left += 1
        if grid[row_index][j] >= height:
            break

    score_right: int = 0
    for j in range(column_index+1, columns_number):
        score_right += 1
        if grid[row_index][j] >= height:
            break
        
    return score_up * score_down * score_left * score_right

if __name__ == '__main__':
    main()