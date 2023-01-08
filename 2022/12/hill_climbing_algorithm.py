'''
https://adventofcode.com/2022/day/12

[1] Fewer steps required to move from S to E: 383
[2] Fewer steps required to move from any 'a' to E: 377

Time Complexity: O(|V| + |E|)
Space Complexity:
- Start points set: O(|V|)
- Queue: O(|V|)
- Visited set: O(|V|)
- Node-Parent map: O(|V|)
Total: O(|V|)
'''

from collections import deque

def main_example():
    grid: list[list[str]] = []
    with open('12/example_input.txt', 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    shortest_path_steps = find_shortest_path_steps(grid, 'S', 'E')
    assert shortest_path_steps == 31, f"Expected 31 steps, actual {shortest_path_steps}"
    
def main():
    grid: list[list[str]] = []
    with open('12/input.txt', 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    shortest_path_steps = find_shortest_path_steps(grid, 'S', 'E')
    print(f"[1] Fewer steps required to move from S to E:", shortest_path_steps)
    shortest_path_steps = find_shortest_path_steps(grid, 'a', 'E')
    print(f"[2] Fewer steps required to move from any 'a' to E:", shortest_path_steps)

    
    
def find_shortest_path_steps(grid: list[list[str]], start_label: str, end_label: str) -> int :
    start_points = find_start_points(grid, start_label)
    queue: deque[tuple[int, int]] = deque(start_points)
    visited: set[tuple[int, int]] = set(start_points)
    node_parent_map: dict[tuple[int, int], tuple[int, int]] = {}
    
    # BFS
    while len(queue) > 0:
        current = queue.popleft() 
        if grid[current[0]][current[1]] == end_label:
            break
        for adj in get_adjacents(grid, current):
            if adj not in visited:
                visited.add(adj)
                queue.append(adj)
                node_parent_map.setdefault(adj, current)
    
    # Count steps in reverse order            
    count_visited: int = 0
    while True:
        node_value = grid[current[0]][current[1]]
        if node_value == start_label:
            break
        current = node_parent_map.get(current)
        count_visited += 1
    return count_visited
       

def find_start_points(grid: list[list[str]], start_label: str) -> set[tuple[int, int]]:
    start_points: set[tuple[int, int]] = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == start_label:
                start_points.add((i, j))
    return start_points

def get_adjacents(grid: list[list[int]], node: tuple[int, int]) -> set[tuple[int, int]]:
    row, col = node
    adjacents_set: set[tuple[int, int]] = set()
    if row > 0:
        adjacents_set.add((row-1, col))
    if row < len(grid) - 1:
        adjacents_set.add((row+1, col))
    if col > 0:
        adjacents_set.add((row, col-1))
    if col < len(grid[row]) - 1:
        adjacents_set.add((row, col+1))
        
    return [adj for adj in adjacents_set if can_step(grid[row][col], grid[adj[0]][adj[1]])]

def can_step(height_start: str, height_end: str):
    height_start = height_start.replace('S', 'a').replace('E', 'z')
    height_end = height_end.replace('S', 'a').replace('E', 'z')
    return ord(height_end)-1 <= ord(height_start)

if __name__ == '__main__':
    main()