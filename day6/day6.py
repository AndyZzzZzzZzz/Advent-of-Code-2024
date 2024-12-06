



matrix = []
with open('day6/example.txt', 'r') as file:
    for line in file:
        matrix.append(list(line.strip()))

n = len(matrix)
m = len(matrix[0])
initial = None
direction = None
for i in range(n):
    for j in range(m):
        if matrix[i][j] == '^':
            initial = (i,j)
            direction = 'up'
            break
        elif matrix[i][j] == 'v':
            initial = (i,j)
            direction = 'down'
            break
        elif matrix[i][j] == '>':
            initial = (i,j)
            direction = 'right'
            break
        elif matrix[i][j] == '<':
            initial = (i,j)
            direction = 'left'
            break


change = {'up': (-1, 0), 'down': (1, 0), 'right': (0,1), 'left': (0, -1)}
directions = ['up', 'right', 'down', 'left']


def loop(mat, x, y, d):
    count = 0

    for i in range(n):
        for j in range(m):
            if (i,j) == (x,y):
                continue
            elif mat[i][j] == '#':
                continue
        
            new_matrix = [row.copy() for row in mat]
            new_matrix[i][j] = '!'

            if sim(new_matrix, x, y, d):
                count += 1
    print(count)

def sim(matrix, x, y, direction):
    pos_set = set()
    dir_idx = directions.index(direction)
    pos_set.add((x, y, directions[dir_idx]))
    while True:
        dx, dy = change[directions[dir_idx]]
        new_x = x + dx
        new_y = y + dy

        if new_x >= n or new_x < 0 or new_y >= m or new_y < 0:
            return False

        if matrix[new_x][new_y] == '#' or matrix[new_x][new_y] == '!':
            dir_idx = (dir_idx + 1)%4
        else:
            x,y = new_x, new_y
            if (x,y, directions[dir_idx]) in pos_set:
                return True 
            pos_set.add((x,y, directions[dir_idx]))

        #print(len(pos_set))

loop(matrix, initial[0], initial[1], direction)