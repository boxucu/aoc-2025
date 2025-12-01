# initial
key = 50
pswd1 = 0
pswd2 = 0

# read list
file_path = "/Users/boxu/Dev/aoc 2025/day_1_input"
with open(file_path, 'r') as file:
    for line in file:
        if line.startswith("L"):
            operation = -int(line[1:])
        elif line.startswith("R"):
            operation = int(line[1:])

        # final location count
        key_new = (key + operation) % 100
        if key_new == 0:
            pswd1 += 1
        
        # passing count
        bound1 = key + operation
        bound2 = key + operation // abs(operation)
        pswd2 += max(bound1, bound2) // 100 - (min(bound1, bound2) - 1) // 100

        # iterate
        key = key_new

# part 1 result
print(pswd1)

# part 2 result
print(pswd2)