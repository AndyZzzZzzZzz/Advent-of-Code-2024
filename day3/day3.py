import re

pattern = r'mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)'
enabled = True 
res = 0
with open('example.txt', 'r') as file:
    content = file.read()
    for match in re.finditer(pattern, content):
        if match.group(1) and match.group(2):
            if enabled:
                x = int(match.group(1))
                y = int(match.group(2))
                res += x * y
        elif match.group(0) == 'do()':
               
            enabled = True
                    
        elif match.group(0) == "don't()":

            enabled = False
    print(res)
    # line = file.read()
    # result = 0
    # matches = re.findall(pattern, line)
    # # for x, y in matches:
    # #     result = result + (int(x) * int(y))
    # for idx, (x_str, y_str) in enumerate(matches, start=1):
    #         x = int(x_str)
    #         y = int(y_str)
    #         product = x * y
    #         result += product
    # print(result)
