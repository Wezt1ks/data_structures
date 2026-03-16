def solve():
    N = int(input().strip())

    if N % 2 == 0 or N % 5 == 0:
        print("NO")
        return

    remainder = 0
    for length in range(1, N + 1):  # до N достаточно, т.к. остатки повторяются
        remainder = (remainder * 10 + 1) % N
        if remainder == 0:
            print('1' * length)
            return
    print("NO")


if __name__ == "__main__":
    solve()
print("Мироненко Егор Сергеевич")
print("гр: 090301-ПОВа-о25")