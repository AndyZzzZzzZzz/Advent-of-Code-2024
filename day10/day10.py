from collections import deque

matrix = []
with open('day10/example.txt', 'r') as file:
    for line in file:
        vec = [int(c) for c in line.strip()]
        matrix.append(vec)

#print(matrix)
q = deque()


row = len(matrix)
col = len(matrix[0])
dic = {}
for i in range(row):
    for j in range(col):
        if matrix[i][j] == 0:
            key = i*col + j
            dic[key] = set()
            
            q.append((i,j,key))

direction = [(-1,0), (0,1), (1,0), (0,-1)]

#print(dic)
count = 0
while len(q) != 0:

    r, c, key = q.pop()
    val = matrix[r][c]
    
    if val == 9:
        count += 1
        dic[key].add((r,c))
        continue

    for i in direction:
        new_r = r + i[0]
        new_c = c + i[1]
        if 0 <= new_r < row and 0 <= new_c < col and matrix[new_r][new_c] == val + 1:
            q.append((new_r, new_c, key))

#print(dic)
# count = 0
# for p in dic.keys():
#     count += len(dic[p])

print(count)