# Day 17

# Part 1
def main() -> None:
    with open("input.txt", "r") as file:
        data = file.read().strip()

    blocks = data.split("\n\n")

    regs = {}
    for line in blocks[0].splitlines():
        key = line.split(" ")[1].split(":")[0]
        value = int(line.split(" ")[-1])
        regs[key] = value

    prog = list(map(int, blocks[1].split(": ")[1].split(",")))
    ptr = 0

    out = []

    while ptr < len(prog) - 1:
        old_ptr = ptr

        opcode = prog[ptr]
        literal_operand = prog[ptr + 1]

        combo_operand = literal_operand
        if combo_operand > 3:
            combo_operand = regs[chr(ord("A") + combo_operand - 4)]

        if opcode == 0:
            regs["A"] = regs["A"] // (2**combo_operand)
        elif opcode == 1:
            regs["B"] = regs["B"] ^ literal_operand
        elif opcode == 2:
            regs["B"] = combo_operand % 8
        elif opcode == 3:
            if regs["A"] != 0:
                ptr = literal_operand
        elif opcode == 4:
            regs["B"] = regs["B"] ^ regs["C"]
        elif opcode == 5:
            out.append(combo_operand % 8)
        elif opcode == 6:
            regs["B"] = regs["A"] // (2**combo_operand)
        elif opcode == 7:
            regs["C"] = regs["A"] // (2**combo_operand)

        if ptr == old_ptr:
            ptr += 2

    print("Part 1:", ",".join(map(str, out)))



if __name__ == "__main__":
    main()

# Part 2
def run(a: int, prog: list[int]) -> list[int]:
    b = 0
    c = 0
    ptr = 0

    out = []

    while ptr < len(prog) - 1:
        old_ptr = ptr

        opcode = prog[ptr]
        literal_operand = prog[ptr + 1]

        combo_operand = literal_operand
        if combo_operand == 4:
            combo_operand = a
        elif combo_operand == 5:
            combo_operand = b
        elif combo_operand == 6:
            combo_operand = c

        if opcode == 0:
            a = a // (2**combo_operand)
        elif opcode == 1:
            b = b ^ literal_operand
        elif opcode == 2:
            b = combo_operand % 8
        elif opcode == 3:
            if a != 0:
                ptr = literal_operand
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            out.append(combo_operand % 8)
        elif opcode == 6:
            b = a // (2**combo_operand)
        elif opcode == 7:
            c = a // (2**combo_operand)

        if ptr == old_ptr:
            ptr += 2

    return out

def main() -> None:
    with open("input.txt", "r") as file:
        data = file.read().strip()

    blocks = data.split("\n\n")
    prog = list(map(int, blocks[1].split(": ")[1].split(",")))

    a = 0
    for i in range(len(prog) - 1, -1, -1):
        target = prog[i:]

        while run(a, prog) != target:
            a += 1

        if i == 0:
            print("Part 2:", a)
        else:
            a *= 8


if __name__ == "__main__":
    main()
