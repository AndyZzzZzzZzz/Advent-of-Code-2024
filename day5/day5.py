
def check(update, rules):
    violation = []
    position = {page: idx for idx, page in enumerate(update)}

    for x, y in rules:
        if x in position and y in position:
            if position[x] >= position[y]:
                violation.append((x,y))
    return violation


def fix(u, rules):
    violate = check(u, rules)
    while violate:
        for x, y in violate:
            idx_x = u.index(x)
            idx_y = u.index(y)
            if idx_x >= idx_y:
                u[idx_x], u[idx_y] = u[idx_y], u[idx_x]
            violate = check(u, rules)
    return u


list1 = []
list2 = []
empty = False
with open('day5/example.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line == "":
            empty = True
            continue
        
        if not empty:
            list1.append(line.strip())
        else:
            list2.append(line.strip())


rules = [tuple(map(int, rule.split('|'))) for rule in list1]
update = [list(map(int, update.split(','))) for update in list2]

correct = []
incorrect = []
res = 0
for idx, u in enumerate(update, 1):
    v = check(u, rules)
    if not v:
        correct.append(u)
        # median = u[len(u)//2]
        # res += median
    else:
        k = fix(u, rules)
        incorrect.append(k)
        median = k[len(k)//2]
        res += median



print(res)


