import math

# ===== Functions =====
class TupleGroups:
    def __init__(self):
        self.groups = {}      # key -> set of tuples
        self.next_key = 0     # next available key number

    def _find_key(self, tup):
        #Return the key whose set contains the tuple, or None.
        for k, s in self.groups.items():
            if tup in s:
                return k
        return None

    def add_pair(self, t1, t2):
        #Process a pair of tuples according to the rules:
        k1 = self._find_key(t1)
        k2 = self._find_key(t2)

        # Case 1: both in same key → do nothing
        if k1 is not None and k1 == k2:
            return

        # Case 2: both in different keys → merge into k1
        if k1 is not None and k2 is not None:
            # merge sets
            self.groups[k1].update(self.groups[k2])
            del self.groups[k2]
            return

        # Case 3: t1 in a set, t2 not in any set → add t2 to k1
        if k1 is not None and k2 is None:
            self.groups[k1].add(t2)
            return

        # Case 4: t2 in a set, t1 not in any set → add t1 to k2
        if k2 is not None and k1 is None:
            self.groups[k2].add(t1)
            return

        # Case 5: neither t1 nor t2 are in any set → create new key
        self.groups[self.next_key] = {t1, t2}
        self.next_key += 1

    def __repr__(self):
        return repr(self.groups)

# ===== Main =====
# Initial
sum1 = 0
sum2 = 0

# Read file
#file_path = "/Users/boxu/Dev/aoc 2025/example_input"
file_path = "/Users/boxu/Dev/aoc 2025/day_8_input"
points = []
with open(file_path, 'r') as file:
    for line in file:
        x, y, z = map(int, line.strip().split(","))
        points.append((x, y, z))
totalnum = len(points)

distances = {}
for i in range(len(points)):
    for j in range(i + 1, len(points)):  # ensures no duplicates and no self-pairs
        p1 = points[i]
        p2 = points[j]

        # Euclidean distance
        dist = math.dist(p1, p2)

        distances[(p1, p2)] = dist

sorted_pairs = sorted(distances.items(), key=lambda x: x[1])
connected_points = TupleGroups()
step = 0
while True:
    (p1, p2) = sorted_pairs[step][0]
    step += 1
    connected_points.add_pair(p1, p2)
    sizes = [len(s) for s in connected_points.groups.values()]
    sorted_sizes = sorted(sizes, reverse=True)
    if step == 1000:
        sum1 += sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]
        # break
    
    if sorted_sizes[0] == totalnum:
        print(p1, p2)
        sum2 += p1[0] * p2[0]
        break

    if step == totalnum * (totalnum - 1) // 2:
        print("impossible to connect all")
        break

# Result
print("answer for part 1 is ", sum1)
print("answer for part 2 is ", sum2)