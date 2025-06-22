
# from collections import deque

# matrix = []
# with open('day12/small.txt', 'r') as file:
#     for line in file:
#         matrix.append([c for c in line.strip()])


# direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# q = deque()
# seen = set()
# row = len(matrix)
# col = len(matrix[0])
# cost = 0

# for i in range(row):
#     for j in range(col):
#         if (i, j) in seen:
#             continue
#         else:
#             q.append((i,j))
#             seen.add((i,j))

#             area = 0
#             points = []
#             points.append((i,j))
#             # parameter = 0
#             # bfs search loop
#             while len(q) != 0:
#                 r, c = q.popleft()

#                 area += 1


#                 #  curr_parameter = 4

#                 for d in direction:
#                     new_r = r + d[0]
#                     new_c = c + d[1]
#                     if 0 <= new_r < row and 0 <= new_c < col and matrix[new_r][new_c] == matrix[r][c]:
#                         #curr_parameter -= 1
#                         if (new_r, new_c) not in seen:
#                             q.append((new_r, new_c))
#                             seen.add((new_r,new_c))
#                             points.append((new_r,new_c))

#             points.sort()

#             # Group coordinates by rows
#             grouped_points = {}
#             for x, y in points:
#                 if x not in grouped_points:
#                     grouped_points[x] = []
#                 grouped_points[x].append((x, y))

#             grouped_points = [grouped_points[key] for key in sorted(grouped_points.keys())]
#             print(grouped_points)  # Print grouped points after each BFS loop
            
#             count = 3
#             for i in range(len(grouped_points)):
#                 for j in range(1, len(grouped_points[i])):
#                     if grouped_points[i][j][1] - grouped_points[i][j-1][1] != 1:
#                         count += 3
#                     else:
            
#             break
#             cost += (area * curr_side)

# print(cost)
from collections import defaultdict

matrix = []
with open('day12/example.txt', 'r') as file:
    for line in file:
        matrix.append([c for c in line.strip()])

row_size = len(matrix)
col_size = len(matrix[0])
connected_components = {}
ans = 0

# direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def dfs(x,y, element,key):
    if x in range(row_size) and y in range(col_size):
        if (x, y) in connected_components:
            return
        if matrix[x][y] == element:
            connected_components[x, y] = key
            for dx, dy in direction:
                dfs(x+dx, y+dy, element, key)

next = 0
for i in range(row_size):
    for j in range(col_size):

        if (i, j) not in connected_components:
            dfs(i, j, matrix[i][j], next)
            next += 1

#print(connected_components)

new_connected_components = defaultdict(set)
for pair, value in connected_components.items():
    new_connected_components[value].add(pair)

#print(new_connected_components)

for component, nodes in new_connected_components.items():
    area = len(nodes)
    perimeter = []
    #perimeter = 0

    for n in nodes:
        for dx, dy in direction:
            nx, ny = n[0] + dx, n[1] + dy

            if nx not in range(row_size) or ny not in range(col_size) or (nx, ny) not in nodes:
                #perimeter += 1
                perimeter.append((n, (nx, ny)))
    
    perimeter = set(perimeter)
    new_perimeter = set()

    for origin_pos, next_pos in perimeter:
        keep = True
        for dx, dy in [(1, 0), (0, 1)]:
            new_pos1 = (origin_pos[0] + dx, origin_pos[1] + dy)
            new_pos2 = (next_pos[0] + dx, next_pos[1] + dy)

            # Corrected condition: Check if the shifted edge exists
            if (new_pos1, new_pos2) in perimeter:
                keep = False
                break  # No need to check further if one condition is met
        if keep:
            new_perimeter.add((origin_pos, next_pos))

    
    ans += area * (len(new_perimeter))
    print(area, len(perimeter), len(new_perimeter))

print(ans)