
# matrix = []
# with open('day15/small.txt', 'r') as file:
#     text = file.read()
#     blocks = text.strip().split('\n\n')

#     for line in blocks[0].split('\n'):  # Split lines in the first block
#         matrix.append([c for c in line])  # Create a list of characters for each line

#     # Process the second block into a list of instructions
#     instructions = list(blocks[1].replace('\n', ''))

# d = {'^' : (-1,0), '>': (0,1), 'v': (1,0), '<': (0,-1)}

with open('day15/example.txt', 'r') as file:
    s = file.read().strip()

ans = res = 0
s1, s2 = s.split("\n\n")
matrix = [list(r) for r in s1.split("\n")]
n, m = len(matrix), len(matrix[0])

# n = len(matrix)
# m = len(matrix[0])
# r = c = 0

# for i in range(n):
#     for j in range(m):
#         if matrix[i][j] == '@':
#             r = i 
#             c = j
#             break

# def simulate(matrix, instructions, d, r, c):

#     for i in instructions:
#         dr, dc = d[i]
#         new_r = r + dr
#         new_c = c + dc

#         if not (0 <= new_r < n and 0 <= new_c < m):
#             continue 

#         target = matrix[new_r][new_c]

#         if target == '#':
#             continue

#         elif target == 'O':
#             # Attempt to push one or more boxes
#             boxes = []
#             push_r, push_c = new_r, new_c

#             # Collect all consecutive boxes in the direction of movement
#             while 0 <= push_r < n and 0 <= push_c < m and matrix[push_r][push_c] == 'O':
#                 boxes.append((push_r, push_c))
#                 push_r += dr
#                 push_c += dc

#             # Check the cell after the last box
#             if not (0 <= push_r < n and 0 <= push_c < m):
#                 # Cannot push boxes out of bounds
#                 continue

#             box_target_cell = matrix[push_r][push_c]

#             if box_target_cell != '.':
#                 # Cannot push boxes into a non-empty cell
#                 continue

#             # All boxes can be pushed; move them
#             for box_r, box_c in reversed(boxes):
#                 matrix[box_r + dr][box_c + dc] = 'O'  # Move box forward
#                 matrix[box_r][box_c] = '@' if (box_r, box_c) == (new_r, new_c) else 'O'

#             # Update the robot's previous position
#             matrix[r][c] = '.'

#             # Update robot's new position
#             matrix[new_r][new_c] = '@'

#             # Update robot's current position
#             r, c = new_r, new_c

#         else:
#             matrix[new_r][new_c] = '@'
#             matrix[r][c] = '.' 
#             r, c = new_r, new_c

#     return matrix

# matrix = simulate(matrix, instructions, d, r, c)

# res = 0
# for i in range(n):
#     for j in range(m):
#         if matrix[i][j] == 'O':
#             res += (i*100 + j)
# print(res)
# # for l in matrix:
# #     print(l)

g2 = []
for row in matrix:
    nrow = []
    for cx in row:
        if cx == '#':
            nrow.append('#')
            nrow.append('#')
        elif cx == 'O':
            nrow.append('[')
            nrow.append(']')
        elif cx == '.':
            nrow.append('.')
            nrow.append('.')
        elif cx == '@':
            nrow.append('@')
            nrow.append('.')
    g2.append(nrow)


for l in g2:
    print(l)
# for l in g2:
#     print(l)
n, m = len(g2), len(g2[0])
r = c = 0

for i in range(n):
    for j in range(m):
        if g2[i][j] == '@':
            r = i 
            c = j
            break

print(r, c)
ins = s2.replace("\n", "")

for idx, move in enumerate(ins):

    dx, dy = {
        '^' : (-1, 0),
        'v': (1, 0),
        '>': (0, 1),
        '<': (0, -1)
    }[move]

    c2m = [(r, c)]
    i = 0
    impos = False
    while i < len(c2m):

        x,y = c2m[i]
        nx, ny = x + dx, y + dy

        if g2[nx][ny] in "O[]":
            if (nx, ny) not in c2m:
                c2m.append((nx, ny))
            if g2[nx][ny] == '[':
                if(nx, ny + 1) not in c2m:
                    c2m.append((nx, ny + 1))
            if g2[nx][ny] == ']':
                if(nx, ny - 1) not in c2m:
                    c2m.append((nx, ny - 1))
        elif g2[nx][ny] == '#':
            impos = True
            break 
        i += 1
    if impos:
        continue

    new_grid = [[g2[i1][j] for j in range(m)] for i1 in range(n)]
    for x,y in c2m:
        new_grid[x][y] = "."
    for x, y in c2m:
        new_grid[x + dx][y + dy] = g2[x][y]
    
    g2 = new_grid
    r += dx
    c += dy

res = 0
for i in range(n):
    for j in range(m):
        if g2[i][j] != '[':
            continue
        res += 100 * i + j
    
print(res)