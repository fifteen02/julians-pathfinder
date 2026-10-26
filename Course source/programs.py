"""Complete teaching functions. Tiny recursive examples are intentionally limited."""
import sys
from functools import lru_cache
MOD = 1_000_000_007

# Lesson 1 recursion warm-up (L1-01 to L1-04).
def countdown(n):
    if n == 0:
        print('Go!')
        return
    print(n)
    countdown(n - 1)

def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)

def sum_squares(n):
    if n == 0:
        return 0
    return n * n + sum_squares(n - 1)

def power2(n):
    if n == 0:
        return 1
    return 2 * power2(n - 1)

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def stairs_slow(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return stairs_slow(n - 1) + stairs_slow(n - 2)

def stairs_cached(n):
    cache = {0: 1}
    def ways(step):
        if step < 0:
            return 0
        if step not in cache:
            cache[step] = ways(step - 1) + ways(step - 2)
        return cache[step]
    return ways(n)

def stairs_table(n):
    ways = [0] * (n + 1)
    ways[0] = 1
    for step in range(1, n + 1):
        ways[step] = ways[step - 1]
        if step >= 2:
            ways[step] += ways[step - 2]
    return ways[n]

def stairs_13(n):
    ways = [0] * (n + 1)
    ways[0] = 1
    for step in range(1, n + 1):
        for jump in (1, 3):
            if step >= jump:
                ways[step] += ways[step - jump]
    return ways[n]

def recursion_demo():
    def descend(n):
        if n == 0:
            return 0
        return 1 + descend(n - 1)
    try:
        descend(sys.getrecursionlimit() + 10)
    except RecursionError:
        return 'Caught RecursionError: too many nested calls.'
    return 'No RecursionError: the limit was not reached.'

def frog_slow(heights):
    def cost(i):
        if i == 0:
            return 0
        one = cost(i - 1) + abs(heights[i] - heights[i - 1])
        if i == 1:
            return one
        two = cost(i - 2) + abs(heights[i] - heights[i - 2])
        return min(one, two)
    return cost(len(heights) - 1)

def frog_cached(heights):
    cache = {0: 0}
    def cost(i):
        if i not in cache:
            one = cost(i - 1) + abs(heights[i] - heights[i - 1])
            answer = one
            if i >= 2:
                two = cost(i - 2) + abs(heights[i] - heights[i - 2])
                answer = min(one, two)
            cache[i] = answer
        return cache[i]
    return cost(len(heights) - 1)

def frog_table(heights):
    best = [0] * len(heights)
    for i in range(1, len(heights)):
        best[i] = best[i - 1] + abs(heights[i] - heights[i - 1])
        if i >= 2:
            two = best[i - 2] + abs(heights[i] - heights[i - 2])
            best[i] = min(best[i], two)
    return best[-1]

def frog_path(heights):
    n = len(heights)
    best = [0] * n
    previous = [-1] * n
    for i in range(1, n):
        best[i] = best[i - 1] + abs(heights[i] - heights[i - 1])
        previous[i] = i - 1
        if i >= 2:
            two = best[i - 2] + abs(heights[i] - heights[i - 2])
            if two < best[i]:
                best[i] = two
                previous[i] = i - 2
    path = []
    i = n - 1
    while i != -1:
        path.append(i)
        i = previous[i]
    path.reverse()
    return best[-1], path

def dice_slow(n):
    if n == 0:
        return 1
    return sum(dice_slow(n - face) for face in range(1, min(6, n) + 1))

def dice_cached(n):
    cache = {0: 1}
    def count(total):
        if total not in cache:
            cache[total] = sum(count(total - face)
                for face in range(1, min(6, total) + 1)) % MOD
        return cache[total]
    return count(n)

def dice_table(n):
    ways = [0] * (n + 1)
    ways[0] = 1
    for total in range(1, n + 1):
        for face in range(1, 7):
            if total >= face:
                ways[total] += ways[total - face]
        ways[total] %= MOD
    return ways[n]

def dice_ring(n):
    recent = [0] * 6
    recent[0] = 1
    for total in range(1, n + 1):
        answer = sum(recent) % MOD
        recent[total % 6] = answer
    return recent[n % 6]

def dice_window(n):
    recent = [0] * 6
    recent[0] = 1
    window = 1
    for total in range(1, n + 1):
        slot = total % 6
        oldest = recent[slot]
        recent[slot] = window
        window = (window - oldest + recent[slot]) % MOD
    return recent[n % 6]

def dice_123(n):
    ways = [0] * (n + 1)
    ways[0] = 1
    for total in range(1, n + 1):
        for face in (1, 2, 3):
            if total >= face:
                ways[total] += ways[total - face]
        ways[total] %= MOD
    return ways[n]

def grid_slow(rows):
    n = len(rows)
    def count(r, c):
        if r < 0 or c < 0 or rows[r][c] == '*':
            return 0
        if r == 0 and c == 0:
            return 1
        return count(r - 1, c) + count(r, c - 1)
    return count(n - 1, n - 1)

def grid_cached(rows):
    n = len(rows)
    @lru_cache(None)
    def count(r, c):
        if r < 0 or c < 0 or rows[r][c] == '*':
            return 0
        if r == 0 and c == 0:
            return 1
        return (count(r - 1, c) + count(r, c - 1)) % MOD
    return count(n - 1, n - 1)

def grid_table(rows):
    n = len(rows)
    paths = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if rows[r][c] == '*':
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                above = paths[r - 1][c] if r > 0 else 0
                left = paths[r][c - 1] if c > 0 else 0
                paths[r][c] = (above + left) % MOD
    return paths[-1][-1]

def tower_cached(bosses):
    n = len(bosses)
    @lru_cache(None)
    def cost(i, friend_turn):
        if i == n:
            return 0
        answer = float('inf')
        for take in (1, 2):
            if i + take <= n:
                pay = sum(bosses[i:i + take]) if friend_turn else 0
                answer = min(answer, pay + cost(i + take, not friend_turn))
        return answer
    return cost(0, True)

def tower_table(bosses):
    n = len(bosses)
    friend = [0] * (n + 1)
    you = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        friend[i] = bosses[i] + you[i + 1]
        you[i] = friend[i + 1]
        if i + 1 < n:
            pay = bosses[i] + bosses[i + 1]
            friend[i] = min(friend[i], pay + you[i + 2])
            you[i] = min(you[i], friend[i + 2])
    return friend[0]

def array_cached(values, m):
    @lru_cache(None)
    def count(i, previous):
        if i == len(values):
            return 1
        answer = 0
        for value in range(1, m + 1):
            if values[i] != 0 and values[i] != value:
                continue
            if i == 0 or abs(value - previous) <= 1:
                answer += count(i + 1, value)
        return answer % MOD
    return count(0, 0)

def array_full(values, m):
    table = [[0] * (m + 2) for _ in values]
    for value in range(1, m + 1):
        if values[0] in (0, value):
            table[0][value] = 1
    for i in range(1, len(values)):
        for value in range(1, m + 1):
            if values[i] in (0, value):
                table[i][value] = (table[i - 1][value - 1] + table[i - 1][value]
                                   + table[i - 1][value + 1]) % MOD
    return sum(table[-1]) % MOD

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

def feast_cached(limit, a, b):
    @lru_cache(None)
    def best(fullness, used_water):
        answer = fullness
        for fruit in (a, b):
            if fullness + fruit <= limit:
                answer = max(answer, best(fullness + fruit, used_water))
        if not used_water:
            answer = max(answer, best(fullness // 2, True))
        return answer
    return best(0, False)

def feast_table(limit, a, b):
    dry = bytearray(limit + 1)
    wet = bytearray(limit + 1)
    dry[0] = 1
    for fullness in range(limit + 1):
        if dry[fullness]:
            for fruit in (a, b):
                if fullness + fruit <= limit:
                    dry[fullness + fruit] = 1
    for fullness in range(limit + 1):
        if dry[fullness]:
            wet[fullness // 2] = 1
    for fullness in range(limit + 1):
        if wet[fullness]:
            for fruit in (a, b):
                if fullness + fruit <= limit:
                    wet[fullness + fruit] = 1
    for fullness in range(limit, -1, -1):
        if dry[fullness] or wet[fullness]:
            return fullness

BEATS = {'H': 'S', 'P': 'H', 'S': 'P'}

def hps_cached(john, budget):
    @lru_cache(None)
    def best(i, left, previous):
        if i == len(john):
            return 0
        answer = 0
        for gesture in 'HPS':
            change = int(previous != '' and gesture != previous)
            if change <= left:
                win = int(BEATS[gesture] == john[i])
                answer = max(answer, win + best(i + 1, left - change, gesture))
        return answer
    return best(0, budget, '')

def hps_table(john, budget):
    if not john:
        return 0
    gestures = 'HPS'
    impossible = -float('inf')
    before = [[impossible] * 3 for _ in range(budget + 1)]
    for g, gesture in enumerate(gestures):
        before[0][g] = int(BEATS[gesture] == john[0])
    for opponent in john[1:]:
        now = [[impossible] * 3 for _ in range(budget + 1)]
        for used in range(budget + 1):
            for g, gesture in enumerate(gestures):
                best_before = before[used][g]
                if used > 0:
                    for old in range(3):
                        if old != g:
                            best_before = max(best_before, before[used - 1][old])
                now[used][g] = best_before + int(BEATS[gesture] == opponent)
        before = now
    return int(max(max(row) for row in before))
