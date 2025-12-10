import re
import time
import numpy as np
import pulp
start_time = time.time()  # Record the start time

# ===== Functions =====
def parse_line(line: str):
    # --- Extract indicator ---
    m = re.search(r"\[([^\]]*)\]", line)
    raw_indicator = m.group(1)  # e.g. ".##."
    # Convert .##. → 0110 then to integer
    nbit = len(raw_indicator)
    binary_str = raw_indicator.replace('#', '1').replace('.', '0')
    indicator_2num = int(binary_str, 2)
    #print(raw_indicator, binary_str, indicator_2num)

    # --- Extract bottons (tuples inside parentheses) ---
    parens = re.findall(r"\(([^)]*)\)", line)
    bottons_2num = set()
    bottons_matrix = []
    for p in parens:
        bits = ['0'] * nbit
        nums = p.split(',')
        nums = [int(x) for x in nums if x.strip() != '']
        for i in nums:
            bits[i] = '1'
        botton_str = "".join(bits)
        botton_2num = int(botton_str, 2)
        botton_list = [int(c) for c in botton_str]
        bottons_2num.add(botton_2num)
        bottons_matrix.append(botton_list)

    # --- Extract joltage numbers ---
    m2 = re.search(r"\{([^}]*)\}", line)
    raw_joltage = m2.group(1)
    joltage = [int(x) for x in raw_joltage.split(',')]

    return indicator_2num, bottons_2num, joltage, bottons_matrix

def light_press_one_botton(lights, bottons_2num):
    new_lights = set()
    for light in lights:
        for botton in bottons_2num:
            new_lights.add(light ^ botton)
    return new_lights

def light_find_min_press(indicator_2num, bottons_2num):
    if indicator_2num == 0:
        return 0
    else:
        press = 1
        lights = bottons_2num.copy()
        while indicator_2num not in lights:
            lights = light_press_one_botton(lights, bottons_2num)
            press += 1
        return press

def solve_min_sum_integer(A, b):
    A = np.array(A)
    b = np.array(b)

    N1, N2 = A.shape
    
    # Create MILP problem
    prob = pulp.LpProblem("Minimize_Sum", pulp.LpMinimize)

    # Integer non-negative variables
    x = [pulp.LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(N2)]

    # Objective: minimize sum(x)
    prob += pulp.lpSum(x)

    # Equality constraints: A x = b
    for i in range(N1):
        prob += pulp.lpSum(A[i, j] * x[j] for j in range(N2)) == b[i]

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Extract solution
    if pulp.LpStatus[prob.status] == "Optimal":
        return np.array([xi.value() for xi in x]), pulp.value(prob.objective)
    else:
        return None, None

# ===== Main =====
# Initial
sum1 = 0
sum2 = 0

# Read file
#file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_10_input"

resolved = 0
with open(file_path, 'r') as file:
    for line in file:
        indicator_2num, bottons_2num, joltage, bottons_matrix = parse_line(line)
        sum1 += light_find_min_press(indicator_2num, bottons_2num)

        AT = np.array(bottons_matrix)
        A = AT.T
        b = np.array(joltage)
        x_opt, min_sum = solve_min_sum_integer(A, b)
        sum2 += min_sum

        resolved += 1
        print("resolved lines: ", resolved)

# Result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)
end_time = time.time()    # Record the end time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")