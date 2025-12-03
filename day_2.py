# initial
sum1 = 0
sum2 = 0

def is_double_repeat(n):
    s = str(n)
    if len(s) % 2 != 0:   # must have even number of digits
        return False
    
    half = len(s) // 2
    return s[:half] == s[half:]

def is_repeated_pattern(n):
    s = str(n)
    # Try every possible substring length that divides the full length
    for L in range(1, len(s)//2 + 1):
        if len(s) % L == 0:               # substring length must divide whole length
            if s == s[:L] * (len(s)//L):  # repeated pattern test
                return True
    return False

# read ranges
file_path = "/Users/boxu/Dev/aoc 2025/day_2_input"
with open(file_path, 'r') as file:
    for line in file:
        # Split the line into ranges separated by commas
        ranges = line.strip().split(",")

        for r in ranges:
            # Split each range into start and end
            ID_0, ID_end = map(int, r.split("-"))
            #print("ID_0 =", ID_0, "   ID_end =", ID_end)
            for n in range (ID_0, ID_end + 1):
                if is_double_repeat(n):
                    sum1 += n
                if is_repeated_pattern(n):
                    sum2 += n

# part 1 result
print(sum1)
# part 2 result
print(sum2)