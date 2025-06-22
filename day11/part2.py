from collections import defaultdict

def transform_stone(number):
    num_str = str(number)
    mid = len(num_str) // 2
    left_half = int(num_str[:mid]) if num_str[:mid] else 0
    right_half = int(num_str[mid:]) if num_str[mid:] else 0
    return left_half, right_half

# Read initial stones
stone_counts = defaultdict(int)
with open('day11/example.txt', 'r') as file:
    for line in file:
        for val_str in line.strip().split():
            if val_str:
                val = int(val_str)
                stone_counts[val] += 1

iterations = 75
for _ in range(iterations):
    new_stone_counts = defaultdict(int)

    for stone_val, count in stone_counts.items():
        if stone_val == 0:
            # Rule 1
            new_stone_counts[1] += count
        elif len(str(stone_val)) % 2 == 0:
            # Rule 2
            a, b = transform_stone(stone_val)
            new_stone_counts[a] += count
            new_stone_counts[b] += count
        else:
            # Rule 3
            new_stone_counts[stone_val * 2024] += count

    stone_counts = new_stone_counts

# After all iterations, count the total stones
total_stones = sum(stone_counts.values())
print(total_stones)
