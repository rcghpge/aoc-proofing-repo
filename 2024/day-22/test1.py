import math
import functools
import time

def _parse_input(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        return [int(_) for _ in file.read().splitlines()]

def _mix(val: int, secret: int) -> int:
    return val ^ secret

def _prune(val: int) -> int:
    return val % 16777216

def _mix_and_prune(val: int, secret: int) -> int:
    return _prune(_mix(val, secret))

def next_secret(secret: int) -> int:
    secret = _mix_and_prune(secret * 64, secret)
    secret = _mix_and_prune(math.floor(secret / 32), secret)
    return _mix_and_prune(secret * 2048, secret)

@functools.cache
def _all_secrets(secret: int) -> list[int]:
    res = [secret]
    cur_val = secret
    for _ in range(2000):
        cur_val = next_secret(cur_val)
        res.append(cur_val)
    return res

def solve_a(file_path: str) -> int:
    return sum(
        _all_secrets(
            _,
        )[-1]
        for _ in _parse_input(file_path)
    )

def _prices(secret: int) -> list[int]:
    return [_ % 10 for _ in _all_secrets(secret)]

def _changes(prices: list[int]) -> list[int]:
    return [_n - _p for _n, _p in zip(prices[1:], prices)]

def _possible_prices(
    prices: list[int], changes: list[int]
) -> dict[tuple[int, int, int, int], int]:
    res = {}
    for _ in range(len(changes) - 3):
        pattern = (changes[_], changes[_ + 1], changes[_ + 2], changes[_ + 3])
        if pattern not in res:
            res[pattern] = prices[_ + 4]
    return res

def solve_b(file_path: str) -> int:
    results: dict[tuple[int, int, int, int], int] = {}
    for _ in _parse_input(file_path):
        prices = _prices(_)
        for _k, _v in _possible_prices(prices, _changes(prices)).items():
            results[_k] = results.get(_k, 0) + _v
    return max(results.values())

if __name__ == "__main__":
    input_file = "input.txt"

    # Timing solve_a
    start_time = time.time()
    result_a = solve_a(input_file)
    end_time = time.time()
    elapsed_time_a = end_time - start_time
    print(f"Solution A: {result_a} (Execution Time: {elapsed_time_a:.3f} seconds)")

    # Timing solve_b
    start_time = time.time()
    result_b = solve_b(input_file)
    end_time = time.time()
    elapsed_time_b = end_time - start_time
    print(f"Solution B: {result_b} (Execution Time: {elapsed_time_b:.3f} seconds)")

