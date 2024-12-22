def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return [int(x) for x in data]


def mix(x, y):
    return x ^ y


def prune(x):
    return x % 16777216


def convert(x):
    y = prune(mix(x, x * 64))
    y = prune(mix(y, y // 32))
    y = prune(mix(y, y * 2048))
    return y


def get_answer(numbers, n):
    res = numbers.copy()
    for _ in range(n):
        res = map(convert, res)
    return sum(res)


def main():
    file = "input.txt"
    secret_numbers = get_data(file)
    asn1 = get_answer(secret_numbers, 2000)
    print(f"{asn1=}")


if __name__ == "__main__":
    assert mix(15, 42) == 37
    assert prune(100000000) == 16113920
    assert convert(123) == 15887950
    assert convert(convert(123)) == 16495136
    main()
