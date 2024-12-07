import operator
import itertools 

def all_ops_sequence(num_operations):
    return list(itertools.product(operations.keys(), repeat=num_operations))

def concat(a, b):
    return int(str(a) + str(b))

operations = {
    '+': operator.add,
    '*': operator.mul,
    '||': concat,
}

def eval(num, ops):
    result = num[0]
    for i, op in enumerate(ops):
        operation = operations[op]
        if i+1 == len(num):
            return result
        next = num[i + 1]
        result = operation(result, next)
    return result 

def all_pattern(data):
    goal = 0
    for key, n in data:
        num_operation = len(n) - 1
        result = 0
        for ops in all_ops_sequence(num_operation):
            result = eval(n, ops)
            if result == key:
                goal += key
                break
    print(goal)


store = []
with open('day7/example.txt') as file:
    for line in file:
        key, value = line.strip().split(':', 1)
        key = int(key)
        sequence = [int(v) for v in value.strip().split()]
        store.append((key, sequence))
#print(store)
all_pattern(store)
# print(store)

