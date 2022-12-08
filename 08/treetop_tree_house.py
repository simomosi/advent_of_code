'''
https://adventofcode.com/2022/day/8

Output
[1] The number of trees visible from outside the grid is 1736
[2] The highest scenic score is 268800

Let n,m be the number of rows/cols of the matrix. In this case n = m

Part 1
Time Complexity: O(4n2) = O(n2)
Space Complexity: O(n2)

Part 2
Time Complexity:  O(n2 * (n+n)) = O(n3)
Space Complexity: O(1)
'''

def main():
    grid: list[list[int]] = []
    with open('08/input.txt', 'r') as file:
        for line in file:
            grid.append(list(map(int, line.strip())))
    # grid = [[3,0,3,7,3], [2,5,5,1,2], [6,5,3,3,2], [3,3,5,4,9], [3,5,3,9,0]]

    rows = len(grid)
    columns = len(grid[0])
    
    visible_trees = count_visibles(grid, rows, columns)
    print(f"[1] The number of trees visible from outside the grid is {visible_trees}")
    
    scenic_scores:list[int] = []
    for i in range(rows):
        for j in range(columns):
            scenic_scores.append(compute_scenic_score(grid, i, j, rows, columns))
            
    print(f"[2] The highest scenic score is {max(scenic_scores)}") # 124 too low

def count_visibles(grid: list[list[int]], rows_number: int, columns_number: int) -> int:
    visible_coordinate_set: set(int, int) = set()
    for i in range(rows_number):
        # Left to right
        local_max = -1
        for j in range(columns_number):
            if grid[i][j] > local_max:
                visible_coordinate_set.add((i,j))
                local_max = grid[i][j]
        # Right to left
        local_max = -1
        for j in range(columns_number-1, -1, -1):
            if grid[i][j] > local_max:
                visible_coordinate_set.add((i,j))
                local_max = grid[i][j]
    
    for j in range(columns_number):
        # Up to down
        local_max = -1
        for i in range(rows_number):
            if grid[i][j] > local_max:
                visible_coordinate_set.add((i,j))
                local_max = grid[i][j]
                
        # Down to up
        local_max = -1
        for i in range(rows_number-1, -1, -1):
            if grid[i][j] > local_max:
                visible_coordinate_set.add((i,j))
                local_max = grid[i][j]
    return len(visible_coordinate_set)

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