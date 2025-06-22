initial = int(input("")) # initial position
n = int(input("")) # length

store = {}
result = ""
for i in range(n):
    word = input("")
    if i == initial:
        result += word
    else:
        if word[0] in store:
            store[word[0]].append(word)
        else:
            store[word[0]] = [word]

while(result[-1] in store):
    array =[i for i in store[result[-1]]]
    array.sort()
    curr_size = 0
    pos = 0
    for i in range(len(array)):
        if len(array[i]) > curr_size:
            curr_size = len(array[i])
            pos = i
    store[result[-1]].remove(array[pos])
    result += array[pos]

print(result)
