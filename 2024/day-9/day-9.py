from collections import deque

f = [x for x in open("input.txt").read().strip().splitlines()]
def checksum(ret):
    p = 0
    for i, val in enumerate(ret):
        if val != ".":
            p += (int(val) * i)
    return p


gaps = {}
v = []
num = 0
val_runs = []
val_runs_dict = {}
for i, val in enumerate(f[0]):
    if i % 2 == 0:
        for j in range(int(val)):
            v.append(num)
        val_runs.append((num, int(val)))
        val_runs_dict[num] = int(val)
        num += 1
    else:
        for j in range(int(val)):
            v.append(".")


def p1():
    ret = []
    q = deque(v)

    while q:
        cur = q.popleft()
        if cur == ".":
            if q:
                while q[-1] == ".":
                    q.pop()
                ret.append(q.pop())
        else:
            ret.append(cur)
    return checksum(ret)
print(p1())


def p2():
    val_runs.reverse()
    i = 0
    while i < len(v):
        if v[i] == ".":
            start = i
            while i < len(v) and v[i] == ".":
                i += 1
            gaps[start] = (i - start)
        else:
            i += 1


    b_val_runs = []
    for val in val_runs:
        b_val_runs.append((v.index(val[0]), val))
    filled_gaps = []
    runs_handled = set()
    filled_gaps_dict = {}
    while gaps:
        something_handled = False
        for i, (value, len_of_val) in b_val_runs:
            if i in runs_handled:
                continue
            candidates = [(k,val) for k,val in gaps.items() if k <= i and val >= len_of_val]
            if len(candidates) == 0:
                continue
            start, length = min(candidates, key=lambda x: x[0])
            filled_gaps.append((start, len_of_val, value))
            filled_gaps_dict[start] = (len_of_val, value)
            runs_handled.add(i)
            something_handled = True
            del gaps[start]
            if length > len_of_val:
                gaps[start + len_of_val] = (length - len_of_val)
        if not something_handled:
            break

    filled_gaps_vals = {x[1] for x in filled_gaps_dict.values()}
    ret = []
    q = deque(v)
    i = 0
    while q and i < len(v):
        if i in filled_gaps_dict:
            for j in range(filled_gaps_dict[i][0]):
                ret.append(str(filled_gaps_dict[i][1]))
                q.popleft()
                # i += 1
            i += filled_gaps_dict[i][0]

        elif q[0] in filled_gaps_vals:
            ret.append('.')
            q.popleft()
            i += 1
        else:
            ret.append(q.popleft())
            i += 1
    return checksum(ret)

print(p2())
