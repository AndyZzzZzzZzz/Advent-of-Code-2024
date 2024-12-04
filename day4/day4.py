
direction = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
diagonal = [(1,1), (1,-1)]


def bfs(grid):
    row = len(grid)
    col = len(grid[0])
    target = "XMAS" # match this target string
    word_len = len(target)
    count = 0

    for r in range(row):
        for c in range(col):
            if(grid[r][c] == target[0]): # start searching once the initial string match 
                for x, y in direction: # traverse all 8 directions 
                    found = True
                    for i in range(1, word_len): # track which letter we are on in the target 
                        new_r = r + x*i
                        new_c = c + y*i
                        # bounds check 
                        if new_r < 0 or new_r >= row or new_c < 0 or new_c >= col:
                            found = False
                            break
                        # macth check 
                        if grid[new_r][new_c] != target[i]:
                            found = False
                            break
                    if found:
                        count += 1
    
    print(count)

goal = ["MAS", "SAM"] # target
# bottom up diagonal matching function 
def search(grid, start_r, start_c, dir, pattern):
    row = len(grid)
    col = len(grid[0])
    length = len(pattern)
    x, y = dir
    # only need to search for 3 position 
    for i in range(length):
        new_r = start_r + x*i
        new_c = start_c + y*i
        # bounds check
        if new_r < 0 or new_r >= row or new_c < 0 or new_c >= col:
            return False
        # match check 
        if grid[new_r][new_c] != pattern[i]:
            return False
    return True

def count(grid):
    row = len(grid)
    col = len(grid[0])
    count = 0
    
    for r in range(row):
        for c in range(col):
            # the search must centered around A
            if grid[r][c] != 'A':
                continue

            for p1 in goal:
                for p2 in goal: 
                    # if both direction matches, X is valid 
                    if(search(grid, r-1, c-1, diagonal[0], p1) and search(grid, r-1, c+1, diagonal[1], p2)):
                        count += 1
    print(count)
grid = []
with open('day4/example.txt', 'r') as file:
     for idx, line in enumerate(file, start=1):
        strip = line.strip() 
        if not strip:
            continue 
        row = list(strip)
        grid.append(row)

count(grid)
