from collections import Counter

# Read initial stones from input file
with open('input.txt') as f:
    initial_stones = [int(x) for x in f.read().split()]

def simulate_blinks(stones_list, blinks):
    stones = Counter(stones_list)
    for _ in range(blinks):
        new_stones = Counter()
        for num, count in stones.items():
            if num == 0:
                # Rule 1: 0 becomes 1
                new_stones[1] += count
            elif len(str(num)) % 2 == 0:
                # Rule 2: Even number of digits, split
                s = str(num)
                mid = len(s) // 2
                left = s[:mid].lstrip('0') or '0'
                right = s[mid:].lstrip('0') or '0'
                new_stones[int(left)] += count
                new_stones[int(right)] += count
            else:
                # Rule 3: Multiply by 2024
                new_num = num * 2024
                new_stones[new_num] += count
        stones = new_stones
    total_stones = sum(stones.values())
    return total_stones

# Part One: 25 blinks
stones_after_25_blinks = simulate_blinks(initial_stones, 25)
print("Part 1: number of stones after 25 blinks:", stones_after_25_blinks)

# Part Two: 75 blinks
stones_after_75_blinks = simulate_blinks(initial_stones, 75)
print("Part 2: number of stones after 75 blinks:", stones_after_75_blinks)
