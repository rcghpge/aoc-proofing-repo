from functools import cmp_to_key
from pathlib import Path
from collections import defaultdict

# Day 5 solution
fn = Path(__file__).parent / "input.txt"
b1, b2 = fn.read_text().strip().split("\n\n")

after_me = defaultdict(list)
before_me = defaultdict(list)
for l in b1.split("\n"):
    p, n = l.split("|")
    after_me[p].append(n)
    before_me[n].append(p)

# Cmp function to return - less than, + greater than, 0 equal
def cmp(a, b):
    if a in after_me and b in after_me[a]:
        return -1
    if a in before_me and b in before_me[a]:
        return 1
    if b in after_me and a in after_me[b]:
        return 1
    if b in before_me and a in before_me[b]:
        return -1

    raise RuntimeError


# Sequence, stick val:idx in dict
# for val, check all after_me values and indices; all before_me indices have small values
valid_sum = 0
repaired_sum = 0
for update in b2.split("\n"):
    # Create dict from page number to position in list
    update_dict = {}
    update_list = update.split(",")
    for i, p in enumerate(update_list):
        update_dict[p] = i

    # Udate dict, check for number of all before_me and after_me constraints
    # Numbers in dict, constraints in dicts
    valid = True
    for p in update_dict:
        if p in after_me:  # constraint
            for ap in after_me[p]:  # ap = after page
                if ap in update_dict and update_dict[ap] <= update_dict[p]:
                    valid = False

        if valid and p in before_me:
            for bp in before_me[p]:
                if bp in update_dict and update_dict[bp] >= update_dict[p]:
                    valid = False

    if valid:
        valid_sum += int(update_list[len(update_list) // 2])

    else:
        sorted_update_list = sorted(update_list, key=cmp_to_key(cmp))
        repaired_sum += int(sorted_update_list[len(sorted_update_list) // 2])

# Part 1:
print(valid_sum)

# Part 2:
print(repaired_sum)
