# ===== Functions =====
def number_in_ranges(n, ranges):
    for (start, end) in ranges:
        low = min(start, end)
        high = max(start, end)
        if low <= n <= high:
            return True
    return False

def merge_ranges(ranges):
    # Convert set to sorted list based on start value
    intervals = sorted(ranges, key=lambda x: x[0])
    merged = []

    for start, end in intervals:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]

            if start <= last_end:     # overlap
                merged[-1][1] = max(last_end, end)
            else:
                merged.append([start, end])

    # Convert back to tuple form
    return {tuple(m) for m in merged}

# ===== Main =====
# initial
sum1 = 0
sum2 = 0

# read file
file_path = "/Users/boxu/Dev/aoc 2025/day_5_input"
ranges = set()
ID_list = set()
with open(file_path, 'r') as file:
    for line in file:
        if line != "\n":
            if "-" in line:
                a, b = line.split("-")
                ranges.add((int(a),int(b)))
            else:
                line_str = line.strip()
                line_num = int(line_str)
                ID_list.add(line_num)

for ID_number in ID_list:
    if number_in_ranges(ID_number, ranges):
        sum1 += 1

new_ranges = merge_ranges(ranges)
for (start, end) in new_ranges:
    sum2 += end - start + 1
 
# result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)