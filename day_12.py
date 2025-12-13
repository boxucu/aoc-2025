import time
start_time = time.time()  # Record the start time

# ===== Functions =====
def check_9x9(row, col, count):
    if sum(count) <= (row // 3) * (col // 3):
        return True

# ===== Main =====
# Initial
sum1 = 0

# Read file
#file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_12_input"

space = []
counts = []
with open(file_path, "r") as file:
    for line in file:
        line = line.strip()
        if "x" in line and ":" in line:
            # split "4x4: 0 0 0 0 2 0"
            left, right = line.split(":")
            row_str, col_str = left.split("x")

            row = int(row_str)
            col = int(col_str)

            nums = list(map(int, right.split()))

            space.append([row, col])
            counts.append(nums)

puzzles = len(space)
for puzzle in range (0, puzzles):
    row, col = space[puzzle]
    if check_9x9(row, col, counts[puzzle]):
        sum1 += 1

# Result
print("answer for part 1 is ", sum1)
end_time = time.time()    # Record the end time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")