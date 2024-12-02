def mono(lst):
    if len(lst) < 2:
        return True
    inc = all(lst[i] < lst[i + 1] for i in range(len(lst) - 1))
    dec = all(lst[i] > lst[i + 1] for i in range(len(lst) - 1))
    return inc or dec

def diff(lst):
    return all(1 <= abs(lst[i] - lst[i + 1]) <= 3 for i in range(len(lst) - 1))

count = 0
with open('levels.txt', 'r') as file:
    for line in file:
        value = line.split()

        int_values = [int(v) for v in value]
        
        if mono(int_values) and diff(int_values):
            count += 1
            continue  

        safe = False
        for i in range(len(int_values)):
            n = int_values[:i] + int_values[i+1:]
            if mono(n) and diff(n):
                count += 1
                safe = True
                break 


print(count)

#       Part one solution

#         unsave = False
#         for i in range(1, len(value)):
#             if abs(int(value[i]) - int(value[i - 1])) < 1 or abs(int(value[i]) - int(value[i - 1])) > 3:
#                unsave = True 
#                break

#         if not unsave:
#           if all(int(value[i]) < int(value[i + 1]) for i in range(len(value) - 1)) or all(int(value[i]) > int(value[i + 1]) for i in range(len(value) - 1)):
#               count += 1

        
            
                
# print(count)
        
            