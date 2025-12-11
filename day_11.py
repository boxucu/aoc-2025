import time
start_time = time.time()  # Record the start time

# ===== Functions =====
def count_paths(connections, start, end):
    memo = {}          # memo[node] = number of paths from node to end
    visited = set()    # nodes currently on the DFS path (prevents loops)

    def dfs(node):
        if node == end:
            return 1
        if node in memo:
            return memo[node]
        if node in visited:
            return 0    # avoid loops

        visited.add(node)

        total = 0
        for nxt in connections.get(node, []):
            total += dfs(nxt)

        visited.remove(node)

        memo[node] = total
        return total

    return dfs(start)

# ===== Main =====
# Initial
sum1 = 0
sum2 = 0

# Read file
#file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_11_input"

connections = {}
with open(file_path, 'r') as file:
    for line in file:
        key, values = line.split(":")
        key = key.strip()
        value_set = set(values.strip().split())
        connections[key] = value_set

sum1 += count_paths(connections, "you", "out")

path_svr_dac = count_paths(connections, "svr", "dac")
path_svr_fft = count_paths(connections, "svr", "fft")
path_dac_out = count_paths(connections, "dac", "out")
path_fft_out = count_paths(connections, "fft", "out")
path_dac_fft = count_paths(connections, "dac", "fft")
path_fft_dac = count_paths(connections, "fft", "dac")

sum2 += path_svr_dac*path_dac_fft*path_fft_out + path_svr_fft*path_fft_dac*path_dac_out

# Result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)
end_time = time.time()    # Record the end time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")