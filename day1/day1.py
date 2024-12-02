
list1 = []
list2 = []

with open('AOC2024/example.txt', 'r') as file:
    for line in file:

        value = line.split()
        list1.append(int(value[0]))
        list2.append(int(value[1]))

list1.sort()
list2.sort()
dictionary = {}

# sum = 0
# for i in range(len(list1)):
#     sum += (abs(list1[i] - list2[i]))

for i in list2:
    if i not in dictionary:
        dictionary[i] = 1
    else:
        dictionary[i] += 1

sim = 0
for i in list1:
    if i in dictionary:
        sim += (i * dictionary[i])


print(sim)