# initial
sum1 = 0
sum2 = 0

def pick_two_largest_in_order(s):
    core = s[:-1]
    # ---- First digit ----
    d1 = max(core)
    i1 = core.index(d1)

    # ---- Second digit ----
    rest = s[i1+1:]
    d2 = max(rest)
    #i2 = i1 + 1 + rest.index(d2)

    return int(d1+d2)

def pick_n_largest_in_order(s,n):
    index = 0
    output = ""
    length = len(s)

    for rank in range (1, n+1):
        core = s[index : length-(n-rank)]
        digit = max(core)
        output += digit
        index += core.index(digit) + 1
    return int(output)

# read file
file_path = "/Users/boxu/Dev/aoc 2025/day_3_input"
with open(file_path, 'r') as file:
    for line in file:
        bank = line.strip()
        sum1 += pick_two_largest_in_order(bank)
        sum2 += pick_n_largest_in_order(bank,12)

# result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)