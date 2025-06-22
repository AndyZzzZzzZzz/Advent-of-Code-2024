# import heapq

# def read_maze(file_path):
#     """
#     Reads the maze from a text file and returns the grid along with start and end positions.
#     """
#     grid = []
#     start = end = None
#     with open(file_path, 'r') as file:
#         for y, line in enumerate(file):
#             row = list(line.rstrip('\n'))
#             for x, char in enumerate(row):
#                 if char == 'S':
#                     start = (x, y)
#                 elif char == 'E':
#                     end = (x, y)
#             grid.append(row)
#     if start is None or end is None:
#         raise ValueError("Maze must have exactly one start 'S' and one end 'E'.")
#     return grid, start, end

# def get_neighbors(position, direction, grid):
#     """
#     Given a position and direction, returns possible next states with their corresponding costs.
#     """
#     directions = ['N', 'E', 'S', 'W']
#     dir_idx = directions.index(direction)
#     neighbors = []
    
#     # Rotate Left (Counterclockwise)
#     new_dir_left = directions[(dir_idx - 1) % 4]
#     neighbors.append(((position, new_dir_left), 1000))
    
#     # Rotate Right (Clockwise)
#     new_dir_right = directions[(dir_idx + 1) % 4]
#     neighbors.append(((position, new_dir_right), 1000))
    
#     # Move Forward
#     move_offsets = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
#     dx, dy = move_offsets[direction]
#     new_x, new_y = position[0] + dx, position[1] + dy
#     if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]):
#         if grid[new_y][new_x] != '#':
#             neighbors.append((( (new_x, new_y), direction), 1))
    
#     return neighbors

# def find_lowest_score(grid, start, end):
#     """
#     Uses Dijkstra's algorithm to find the lowest score from start to end.
#     """
#     import sys
#     directions = ['N', 'E', 'S', 'W']
#     # Initial state: position, direction, score
#     initial_direction = 'E'  # Facing East initially
#     heap = []
#     heapq.heappush(heap, (0, start, initial_direction))
    
#     # Visited dictionary: (position, direction) -> score
#     visited = {}
    
#     while heap:
#         score, position, direction = heapq.heappop(heap)
        
#         if (position, direction) in visited:
#             continue
#         visited[(position, direction)] = score
        
#         if position == end:
#             return score
        
#         for (next_state, cost) in get_neighbors(position, direction, grid):
#             next_pos, next_dir = next_state
#             if (next_pos, next_dir) not in visited:
#                 heapq.heappush(heap, (score + cost, next_pos, next_dir))
    
#     return sys.maxsize  # If end is not reachable

# def main():
    
#     grid, start, end = read_maze('day16/example.txt')
#     lowest_score = find_lowest_score(grid, start, end)
    
#     if lowest_score != float('inf'):
#         print(f"The lowest score a Reindeer could possibly get is: {lowest_score}")
#     else:
#         print("No path found from Start to End.")

# if __name__ == "__main__":
#     main()

import heapq
import sys
import argparse
from collections import defaultdict, deque

def read_maze(file_path):
    grid = []
    start = end = None
    with open(file_path, 'r') as file:
        for y, line in enumerate(file):
            row = list(line.rstrip('\n'))
            for x, char in enumerate(row):
                if char == 'S':
                    if start is not None:
                        raise ValueError("Maze must have exactly one start 'S'.")
                    start = (x, y)
                elif char == 'E':
                    if end is not None:
                        raise ValueError("Maze must have exactly one end 'E'.")
                    end = (x, y)
            grid.append(row)
    if start is None or end is None:
        raise ValueError("Maze must have exactly one start 'S' and one end 'E'.")
    return grid, start, end

def get_neighbors(position, direction, grid):
    directions = ['N', 'E', 'S', 'W']
    dir_idx = directions.index(direction)
    neighbors = []
    
    # Rotate Left (Counterclockwise)
    new_dir_left = directions[(dir_idx - 1) % 4]
    neighbors.append(((position, new_dir_left), 1000, 'rotate'))
    
    # Rotate Right (Clockwise)
    new_dir_right = directions[(dir_idx + 1) % 4]
    neighbors.append(((position, new_dir_right), 1000, 'rotate'))
    
    # Move Forward
    move_offsets = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
    dx, dy = move_offsets[direction]
    new_x, new_y = position[0] + dx, position[1] + dy
    if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]):
        if grid[new_y][new_x] != '#':
            neighbors.append((( (new_x, new_y), direction), 1, 'move'))
    
    return neighbors

def find_lowest_score_and_predecessors(grid, start, end):
    directions = ['N', 'E', 'S', 'W']
    initial_direction = 'E'  # Facing East initially
    
    # dist: best known score for each state (position, direction)
    dist = defaultdict(lambda: sys.maxsize)
    dist[(start, initial_direction)] = 0
    
    heap = []
    heapq.heappush(heap, (0, start, initial_direction))
    
    # visited: set states that are finalized (no better path will be found)
    visited = {}
    
    # predecessors: minimal path predecessors for each state
    predecessors = defaultdict(list)
    
    while heap:
        score, position, direction = heapq.heappop(heap)
        
        if (position, direction) in visited:
            continue
        
        visited[(position, direction)] = score
        
        for (next_state, cost, action) in get_neighbors(position, direction, grid):
            next_pos, next_dir = next_state
            new_score = score + cost
            
            if new_score < dist[(next_pos, next_dir)]:
                # Found a strictly better path
                dist[(next_pos, next_dir)] = new_score
                predecessors[(next_pos, next_dir)] = [(position, direction, action)]
                heapq.heappush(heap, (new_score, next_pos, next_dir))
            elif new_score == dist[(next_pos, next_dir)]:
                # Found another equally good path
                predecessors[(next_pos, next_dir)].append((position, direction, action))
                # Note: no need to push to heap since it's already known minimal
                
    # Find the minimal score to reach the end (in any direction)
    min_score = sys.maxsize
    end_states = []
    for dir in directions:
        state = (end, dir)
        if state in visited:
            if visited[state] < min_score:
                min_score = visited[state]
                end_states = [state]
            elif visited[state] == min_score:
                end_states.append(state)
    
    if min_score == sys.maxsize:
        return min_score, None, None, None
    
    return min_score, predecessors, end_states, visited

def backtrack_and_count_paths(predecessors, end_states, start, visited):
    path_length_counts = defaultdict(int)
    queue = deque()
    
    for state in end_states:
        queue.append((state, 0))
    
    while queue:
        current_state, current_length = queue.popleft()
        current_pos, current_dir = current_state
        
        if current_pos == start and current_dir == 'E':
            path_length_counts[current_length] += 1
            continue
        
        for pred in predecessors.get(current_state, []):
            pred_pos, pred_dir, action = pred
            # All actions increase path length by 1
            new_length = current_length + 1
            queue.append(((pred_pos, pred_dir), new_length))
    
    return path_length_counts

def find_best_path_tiles(grid, start, end):
    min_score, predecessors, end_states, visited = find_lowest_score_and_predecessors(grid, start, end)
    
    if min_score == sys.maxsize:
        return min_score, set(), {}
    
    best_tiles = set()
    path_length_counts = backtrack_and_count_paths(predecessors, end_states, start, visited)
    
    # Backtrack again to find all tiles in best paths
    queue = deque(end_states)
    visited_tiles = set(end_states)
    
    while queue:
        current_state = queue.popleft()
        current_pos, current_dir = current_state
        best_tiles.add(current_pos)
        
        if current_pos == start and current_dir == 'E':
            continue
        
        for pred in predecessors.get(current_state, []):
            pred_state = (pred[0], pred[1])
            if pred_state not in visited_tiles:
                visited_tiles.add(pred_state)
                queue.append(pred_state)
    
    return min_score, best_tiles, path_length_counts

def mark_best_path_tiles_detailed(grid, best_tiles):
    marked_grid = [row.copy() for row in grid]
    for y, row in enumerate(marked_grid):
        for x, char in enumerate(row):
            if (x, y) in best_tiles:
                if char not in ('S', 'E', '#'):
                    marked_grid[y][x] = 'O'
    return marked_grid

def main():
    # For demonstration, using 'day16/example.txt', change as needed
    grid, start, end = read_maze('day16/small.txt')
    min_score, best_tiles, path_length_counts = find_best_path_tiles(grid, start, end)
    
    if min_score != sys.maxsize:
        print(f"The lowest score a Reindeer could possibly get is: {min_score}")
        print(f"Number of tiles part of at least one best path: {len(best_tiles)}")
        print(f"Number of optimal paths: {sum(path_length_counts.values())}")
        
        if path_length_counts:
            print("\nDistribution of Path Lengths (Number of Actions):")
            for length in sorted(path_length_counts):
                print(f"Path Length {length}: {path_length_counts[length]} path(s)")
    else:
        print("No path found from Start to End.")
        return

if __name__ == "__main__":
    main()
