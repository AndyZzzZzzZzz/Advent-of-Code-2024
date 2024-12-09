from math import gcd

def find_nodes(grid):
    r = len(grid)
    c = len(grid[0])

    antennas = {}
    for i in range(r):
        for j in range(c):
            if grid[i][j] != '.':
                antennas.setdefault(grid[i][j], []).append((i, j))

    def calc_pos(a, b):
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay
        g = gcd(dx, dy)

        dx //= g
        dy //= g

        all_valid_nodes = []
        # Move forward and backward along the line
        for i in range(1, max(r, c)):
            # Forward direction
            p1 = (ax + i*dx, ay + i*dy)
            if 0 <= p1[0] < r and 0 <= p1[1] < c:
                all_valid_nodes.append(p1)
            else:
                # If out of bounds, no need to keep going in this direction
                pass

            # Backward direction
            p2 = (ax - i*dx, ay - i*dy)
            if 0 <= p2[0] < r and 0 <= p2[1] < c:
                all_valid_nodes.append(p2)
            else:
                # If out of bounds, no need to keep going in this direction
                pass

        return all_valid_nodes
    
    res_pos = set()
    for freq, ann in antennas.items():
        # If only one antenna of this frequency, no line formed, so skip
        if len(ann) < 2:
            continue
        
        # Each antenna is also an antinode for this frequency since there's at least two
        for antenna in ann:
            res_pos.add(antenna)
            
        n = len(ann)
        for i in range(n):
            for j in range(i + 1, n):
                a = ann[i]
                b = ann[j]
                pair_nodes = calc_pos(a, b)
                for p in pair_nodes:
                    res_pos.add(p)

    print(len(res_pos))


# Example usage:
matrix = []
with open('day8/example.txt', 'r') as file:
    for line in file:
        matrix.append(list(line.strip()))

find_nodes(matrix)
