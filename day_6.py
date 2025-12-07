# ===== Functions =====
def multiply_tuple_elements(my_tuple):
    result = 1
    for item in my_tuple:
        result *= item
    return result

# ===== Main =====
# Initial
sum1 = 0
sum2 = 0

# Read file
# file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_6_input"

# Part 1
plus_set = set()
star_set = set()
with open(file_path, 'r') as f:
    lines = [line.rstrip().split() for line in f]

# Separate last-line symbols and the number rows
symbols = lines[-1]
number_rows = lines[:-1]

# Transpose columns
columns = list(zip(*number_rows))

for col_values, symbol in zip(columns, symbols):
    # Convert each value in the column to int
    values = tuple(int(v) for v in col_values)

    if symbol == "+":
        plus_set.add(values)
        sum1 += sum(values)
    elif symbol == "*":
        star_set.add(values)
        sum1 += multiply_tuple_elements(values)

# Part 2
plus_set = set()
star_set = set()

with open(file_path, "r") as f:
    # Read all lines keeping spaces (only strip newline)
    lines = [line.rstrip("\n") for line in f if line.rstrip("\n") != ""]

if len(lines) < 2:
    raise ValueError("File must contain at least one digit row and one symbol row.")

# Pad every line to same width so columns align
width = max(len(line) for line in lines)
lines = [line.ljust(width) for line in lines]

# Reverse all rows
lines = [line[::-1] for line in lines]
# print(lines)

# Last line is the symbols row
symbols = lines[-1]
digit_rows = lines[:-1]

# For each column index, build integer from top->bottom digits (ignore spaces)
number_cols = []
for col in range(width):
    chars = [row[col] for row in digit_rows]            # characters down this column
    digit_str = "".join(ch for ch in chars if ch.isdigit())  # keep only digit chars
    number = int(digit_str) if digit_str else 0
    number_cols.append(number)

# Read columns form tuple
values = tuple()
for col in range(width):
    if number_cols[col] != 0:
        values += (number_cols[col],)  

    if symbols[col] == "+":
        plus_set.add(values)
        sum2 += sum(values)
        values = tuple()
    elif symbols[col] == "*":
        star_set.add(values)
        sum2 += multiply_tuple_elements(values)
        values = tuple()

# print("Plus set:", plus_set)
# print("Star set:", star_set)

# Result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)