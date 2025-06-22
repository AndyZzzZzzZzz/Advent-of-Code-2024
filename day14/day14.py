# import re

# def read_robot_data(filename):
#     """
#     Reads robot positions and velocities from a file.
    
#     Each line in the file should be in the format: p=x,y v=dx,dy
#     """
#     robots = []
#     pattern = re.compile(r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)')
    
#     with open(filename, 'r') as file:
#         for line in file:
#             match = pattern.match(line.strip())
#             if match:
#                 x, y, dx, dy = map(int, match.groups())
#                 robots.append({'x': x, 'y': y, 'dx': dx, 'dy': dy})
#             else:
#                 print(f"Line skipped due to incorrect format: {line.strip()}")
#     return robots

# def simulate_robots(robots, width, height, seconds):
#     """
#     Simulates robot movements over a specified number of seconds with wrapping.
    
#     Args:
#     - robots: List of dictionaries with keys 'x', 'y', 'dx', 'dy'
#     - width: Width of the grid
#     - height: Height of the grid
#     - seconds: Number of seconds to simulate
#     """
#     for robot in robots:
#         # Update positions with wrapping
#         robot['x'] = (robot['x'] + robot['dx'] * seconds) % width
#         robot['y'] = (robot['y'] + robot['dy'] * seconds) % height
#     return robots

# def count_quadrants(robots, width, height):
#     """
#     Counts the number of robots in each quadrant.
    
#     Returns a list with counts [Q1, Q2, Q3, Q4]
#     """
#     center_x = width // 2  # 101 // 2 = 50
#     center_y = height // 2 # 103 // 2 = 51
    
#     Q1 = Q2 = Q3 = Q4 = 0
    
#     for robot in robots:
#         x, y = robot['x'], robot['y']
#         # Exclude robots on the center lines
#         if x == center_x or y == center_y:
#             continue
#         if x < center_x and y < center_y:
#             Q1 += 1
#         elif x > center_x and y < center_y:
#             Q2 += 1
#         elif x < center_x and y > center_y:
#             Q3 += 1
#         elif x > center_x and y > center_y:
#             Q4 += 1
#     return [Q1, Q2, Q3, Q4]

# def calculate_safety_factor(quadrant_counts):
#     """
#     Calculates the safety factor by multiplying the counts of all quadrants.
#     """
#     safety_factor = 1
#     for count in quadrant_counts:
#         safety_factor *= count
#     return safety_factor

# def main():
#     # Parameters
#     filename = 'day14/example.txt'  # Change this if your file has a different name
#     width = 101
#     height = 103
#     simulation_seconds = 100
    
#     # Step 1: Read robot data
#     robots = read_robot_data(filename)
#     if not robots:
#         print("No valid robot data found. Exiting.")
#         return
    
#     # Step 2: Simulate robot movements
#     robots = simulate_robots(robots, width, height, simulation_seconds)
    
#     # Step 3: Count robots in each quadrant
#     quadrant_counts = count_quadrants(robots, width, height)
#     Q1, Q2, Q3, Q4 = quadrant_counts
#     print(f"Quadrant Counts after {simulation_seconds} seconds:")
#     print(f"Quadrant 1 (Top-Left): {Q1}")
#     print(f"Quadrant 2 (Top-Right): {Q2}")
#     print(f"Quadrant 3 (Bottom-Left): {Q3}")
#     print(f"Quadrant 4 (Bottom-Right): {Q4}")
    
#     # Step 4: Calculate safety factor
#     safety_factor = calculate_safety_factor(quadrant_counts)
#     print(f"\nSafety Factor: {safety_factor}")

# if __name__ == "__main__":
#     main()

import re
import os
import time
from collections import defaultdict

def read_robot_data(filename):
    """
    Reads robot positions and velocities from a file.
    
    Each line in the file should be in the format: p=x,y v=dx,dy
    """
    robots = []
    pattern = re.compile(r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)')
    
    with open(filename, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                x, y, dx, dy = map(int, match.groups())
                robots.append({'x': x, 'y': y, 'dx': dx, 'dy': dy})
            else:
                print(f"Line skipped due to incorrect format: {line.strip()}")
    return robots

def simulate_one_second(robots, width, height):
    """
    Simulates one second of robot movement with wrapping.
    
    Args:
    - robots: List of dictionaries with keys 'x', 'y', 'dx', 'dy'
    - width: Width of the grid
    - height: Height of the grid
    """
    for robot in robots:
        robot['x'] = (robot['x'] + robot['dx']) % width
        robot['y'] = (robot['y'] + robot['dy']) % height

def count_quadrants(robots, width, height):
    """
    Counts the number of robots in each quadrant.
    
    Returns a list with counts [Q1, Q2, Q3, Q4]
    """
    center_x = width // 2  # 101 // 2 = 50
    center_y = height // 2 # 103 // 2 = 51
    
    Q1 = Q2 = Q3 = Q4 = 0
    
    for robot in robots:
        x, y = robot['x'], robot['y']
        # Exclude robots on the center lines
        if x == center_x or y == center_y:
            continue
        if x < center_x and y < center_y:
            Q1 += 1
        elif x > center_x and y < center_y:
            Q2 += 1
        elif x < center_x and y > center_y:
            Q3 += 1
        elif x > center_x and y > center_y:
            Q4 += 1
    return [Q1, Q2, Q3, Q4]

def calculate_safety_factor(quadrant_counts):
    """
    Calculates the safety factor by multiplying the counts of all quadrants.
    """
    safety_factor = 1
    for count in quadrant_counts:
        safety_factor *= count
    return safety_factor

def print_grid(robots, width, height):
    """
    Prints the grid with robot positions marked and returns the grid lines.
    
    - '.' represents an empty tile.
    - '#' represents one robot.
    - Numbers represent multiple robots on the same tile.
    
    Returns:
    - grid_lines: List of strings for each row in the grid.
    """
    # Initialize grid with dots
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    # Count robots on each tile
    position_counts = defaultdict(int)
    for robot in robots:
        position_counts[(robot['x'], robot['y'])] += 1
    
    # Mark robots on the grid
    for (x, y), count in position_counts.items():
        if count == 1:
            grid[y][x] = '#'
        else:
            grid[y][x] = str(count)
    
    # Convert grid to list of strings
    grid_lines = [''.join(row) for row in grid]
    
    # Print the grid
    #for line in grid_lines:
        #print(line)
    
    return grid_lines

def find_large_clusters(robots, width, height, min_size=10):
    """
    Identifies all clusters of robots connected in 8 directions with size >= min_size.
    
    Args:
    - robots: List of dictionaries with keys 'x' and 'y'.
    - width: Width of the grid.
    - height: Height of the grid.
    - min_size: Minimum number of robots to qualify as a large cluster.
    
    Returns:
    - clusters: List of sets, each containing positions (x, y) of a large cluster.
    """
    occupied = set((robot['x'], robot['y']) for robot in robots)
    visited = set()
    clusters = []
    
    for pos in occupied:
        if pos in visited:
            continue
        # Start BFS
        queue = [pos]
        cluster = set()
        while queue:
            current = queue.pop(0)  # FIFO queue
            if current in visited:
                continue
            visited.add(current)
            cluster.add(current)
            x, y = current
            # Check all 8 neighbors with wrapping
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor_x = (x + dx) % width
                    neighbor_y = (y + dy) % height
                    neighbor = (neighbor_x, neighbor_y)
                    if neighbor in occupied and neighbor not in visited:
                        queue.append(neighbor)
        if len(cluster) > min_size:
            clusters.append(cluster)
    return clusters

def main():
    # Parameters
    filename = 'day14/example.txt'  # Change this if your file has a different name
    width = 101
    height = 103
    simulation_seconds = 100000
    pause_duration = 1.5  # seconds
    
    # Step 1: Read robot data
    robots = read_robot_data(filename)
    # Step 5: Generate puzzle input for part2
    #puzzle_input = '\n'.join(print_grid(robots, width, height))
    #total_cost = part2(puzzle_input)
    #print(f"\nTotal Cost from part2: {total_cost}")

    if not robots:
        print("No valid robot data found. Exiting.")
        return
    
    # # Step 2: Simulate robot movements with visualization
    # for second in range(1, 1949):
    #     simulate_one_second(robots, width, height)
        
    #     # Clear the terminal
    #     os.system('cls' if os.name == 'nt' else 'clear')
        
    #     # Print current second
    #     #print(f"Second: {second}/{simulation_seconds}\n")
        
    #     if second == 1948:
    #     # Print the grid
    #         print_grid(robots, width, height)
        
    #     # Pause for 1.5 seconds
    #     #time.sleep(pause_duration)
    for second in range(1, simulation_seconds + 1):
        simulate_one_second(robots, width, height)
        
        # Clear the terminal
        #os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print current second
        #print(f"Second: {second}/{simulation_seconds}\n")
        
        # Get the grid lines and print the grid
        grid_lines = print_grid(robots, width, height)
        
        # Check for large clusters
        large_clusters = find_large_clusters(robots, width, height, 50)
        if large_clusters:
            print(f"\n*** Large Cluster Detected at Second {second} ***")
            for idx, cluster in enumerate(large_clusters, start=1):
                print(f"Cluster {idx}: {len(cluster)} robots")
            # Print the grid display
            print("\nGrid Display at Detection:")
            for line in grid_lines:
                print(line)
            # Terminate the simulation
            break
        
        # Pause for 1.5 seconds
        #time.sleep(pause_duration)
    
    # # Step 3: Count robots in each quadrant after simulation
    # quadrant_counts = count_quadrants(robots, width, height)
    # Q1, Q2, Q3, Q4 = quadrant_counts
    # print(f"\nQuadrant Counts after {simulation_seconds} seconds:")
    # print(f"Quadrant 1 (Top-Left): {Q1}")
    # print(f"Quadrant 2 (Top-Right): {Q2}")
    # print(f"Quadrant 3 (Bottom-Left): {Q3}")
    # print(f"Quadrant 4 (Bottom-Right): {Q4}")
    
    # # Step 4: Calculate safety factor
    # safety_factor = calculate_safety_factor(quadrant_counts)
    # print(f"\nSafety Factor: {safety_factor}")

if __name__ == "__main__":
    main()
