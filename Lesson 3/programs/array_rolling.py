MOD = 1_000_000_007

def array_rolling(values, m):
    before = [0] * (m + 2)
    for value in range(1, m + 1):
        if values[0] in (0, value):
            before[value] = 1
    for i in range(1, len(values)):
        now = [0] * (m + 2)
        for value in range(1, m + 1):
            if values[i] in (0, value):
                now[value] = (before[value - 1] + before[value]
                              + before[value + 1]) % MOD
        before = now
    return sum(before) % MOD

n, m = map(int, input().split())
values = list(map(int, input().split()))
print(array_rolling(values, m))
