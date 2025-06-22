


stones = []
with open('day11/example.txt', 'r') as file:
    for line in file:
        
        stones.extend([int(i) for i in line.strip().split() if i])

#print(stones)

def transform_stone(number):
    num_str = str(number)

    mid = len(num_str) // 2
    left_half = int(num_str[:mid])
    right_half = int(num_str[mid:])
    return left_half, right_half
    
for i in range(75):
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif len(str(s)) % 2 == 0:
            a,b = transform_stone(s)
            new_stones.append(a)
            new_stones.append(b)
        else:
            new_stones.append(s * 2024)
    #print(new_stones)
    stones = new_stones

print(len(new_stones))
