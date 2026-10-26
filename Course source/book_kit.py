"""Measured facts for the tutor books.

Every number that a tutor book prints about running code (call counts, how often a
line runs, traced tables, the output of a common mistake) is computed here by
running programs.py, so the books cannot drift from the code. verify_books.py
re-checks these values against closed forms and brute force.
"""
import inspect, sys, time, random
import programs as P

PROGRAMS_FILE = inspect.getsourcefile(P)


def comma(x):
    return f'{x:,}'


def big(x):
    """Counts too large to print in full are described by their number of digits."""
    if isinstance(x, str):
        return x
    return comma(x) if x < 10**15 else f'a {len(str(x)):,}-digit number'


# ---------------------------------------------------------------- instrumentation
def calls(fn, args, inner=None):
    """Number of calls of `inner` (a function name, default the function itself)
    while running fn(*args). Counted with sys.setprofile, so programs.py is untouched."""
    inner = inner or fn.__name__
    count = 0
    def profile(frame, event, arg):
        nonlocal count
        if event == 'call' and frame.f_code.co_name == inner and frame.f_code.co_filename == PROGRAMS_FILE:
            count += 1
    old = sys.getrecursionlimit(); sys.setrecursionlimit(max(old, 10000))
    sys.setprofile(profile)
    try:
        fn(*args)
    finally:
        sys.setprofile(None); sys.setrecursionlimit(old)
    return count


def listing_offset(name):
    """Lines that precode() prints before the def line (imports, constants, blanks)."""
    import build_course as B
    text = B.precode(name).splitlines()
    return next(i for i, line in enumerate(text) if line.startswith('def '))


def line_runs(name, args):
    """{listing line number: times executed} for programs.<name>(*args).
    Line numbers are those printed beside the listing in the book."""
    fn = getattr(P, name)
    lines, start = inspect.getsourcelines(fn)
    end = start + len(lines) - 1
    shift = listing_offset(name) - start + 1
    hits = {}
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != PROGRAMS_FILE:
            return None
        if event == 'line' and start <= frame.f_lineno <= end:
            k = frame.f_lineno + shift
            hits[k] = hits.get(k, 0) + 1
        return tracer
    old = sys.getrecursionlimit(); sys.setrecursionlimit(max(old, 10000))
    sys.settrace(tracer)
    try:
        fn(*args)
    finally:
        sys.settrace(None); sys.setrecursionlimit(old)
    return hits


def listing_line(name, text):
    """Printed line number of the first listing line containing `text`;
    text may be (snippet, k) for the k-th such line (1-based)."""
    import build_course as B
    text, k = text if isinstance(text, tuple) else (text, 1)
    for i, line in enumerate(B.precode(name).splitlines(), 1):
        if text in line:
            k -= 1
            if k == 0:
                return i
    raise KeyError((name, text))


def seconds(fn, args, repeat=1):
    best = None
    for _ in range(repeat):
        t = time.perf_counter(); fn(*args); t = time.perf_counter() - t
        best = t if best is None else min(best, t)
    return best


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


# ---------------------------------------------------------------- mistakes
def run_variant(source, call):
    """Run a deliberately wrong variant and describe what it does."""
    space = {'MOD': P.MOD, 'BEATS': P.BEATS, 'lru_cache': P.lru_cache, 'sys': sys}
    exec(source, space)
    old = sys.getrecursionlimit(); sys.setrecursionlimit(3000)
    try:
        return repr(eval(call, space))
    except RecursionError:
        return 'RecursionError'
    except IndexError:
        return 'IndexError'
    except Exception as e:  # pragma: no cover - reported in the book as it happens
        return type(e).__name__
    finally:
        sys.setrecursionlimit(old)


def variant(name, old, new, call, count=1):
    """programs.<name> with one textual change, run on `call`."""
    src = inspect.getsource(getattr(P, name))
    assert src.count(old) >= count, (name, old)
    return run_variant(src.replace(old, new, count), call)


# ---------------------------------------------------------------- Lesson 1 traces
def stairs_routes(n, jumps=(1, 2)):
    """Every ordered list of jumps that lands exactly on step n."""
    if n == 0:
        return [[]]
    return [r + [j] for j in jumps if j <= n for r in stairs_routes(n - j, jumps)]


def stairs_slow_trace(n):
    """Rows (order, call, asks, returns) in the order Python makes the calls."""
    rows = []
    def go(k, depth):
        row = [str(len(rows) + 1), '. ' * depth + f'stairs_slow({k})', '', '']
        rows.append(row)
        if k < 0:
            row[2] = 'nothing: k < 0'; value = 0
        elif k == 0:
            row[2] = 'nothing: k = 0'; value = 1
        else:
            a = go(k - 1, depth + 1); b = go(k - 2, depth + 1)
            row[2] = f'stairs_slow({k-1}) + stairs_slow({k-2}) = {a} + {b}'; value = a + b
        row[3] = str(value)
        return value
    assert go(n, 0) == P.stairs_slow(n)
    return rows


def stairs_fill(n, jumps=(1, 2)):
    """Rows (step, reads, arithmetic, ways[step]) for a forward table."""
    ways = [0] * (n + 1); ways[0] = 1
    rows = [['0', 'nothing: the empty route', 'start value', '1']]
    for step in range(1, n + 1):
        parts = [step - j for j in jumps if step >= j]
        ways[step] = sum(ways[p] for p in parts)
        reads = ' + '.join(f'ways[{p}]' for p in parts)
        rows.append([str(step), reads, ' + '.join(str(ways[p]) for p in parts), str(ways[step])])
    fn = P.stairs_table if tuple(jumps) == (1, 2) else P.stairs_13
    assert ways[n] == fn(n)
    return rows


def frog_all_routes(h):
    def walk(i):
        if i == len(h) - 1:
            return [[i]]
        return [[i] + r for j in (i + 1, i + 2) if j < len(h) for r in walk(j)]
    out = []
    for r in walk(0):
        costs = [abs(h[b] - h[a]) for a, b in zip(r, r[1:])]
        out.append((r, costs, sum(costs)))
    assert min(c for *_, c in out) == P.frog_table(h)
    return out


def frog_best_route(h):
    r, _, c = min(frog_all_routes(h), key=lambda x: (x[2], len(x[0])))
    return r, c


def frog_greedy(h, rows=None):
    """Cheaper next jump; a tie goes to the farther stone."""
    i, route, total = 0, [0], 0
    while i < len(h) - 1:
        options = [(abs(h[j] - h[i]), -j, j) for j in (i + 1, i + 2) if j < len(h)]
        cost, _, j = min(options)
        if rows is not None:
            rows.append([str(i), ';  '.join(f'to {k}: |{h[k]} − {h[i]}| = {abs(h[k]-h[i])}' for _, _, k in options), str(j), str(total + cost)])
        route.append(j); total += cost; i = j
    return route, total


def frog_fill(h):
    """Rows (stone, height, from i-1, from i-2, best[i])."""
    best = [0] * len(h)
    rows = [['0', str(h[0]), 'start', '—', '0']]
    for i in range(1, len(h)):
        one = best[i - 1] + abs(h[i] - h[i - 1])
        a = f'{best[i-1]} + |{h[i]} − {h[i-1]}| = {one}'
        if i >= 2:
            two = best[i - 2] + abs(h[i] - h[i - 2])
            b = f'{best[i-2]} + |{h[i]} − {h[i-2]}| = {two}'
            best[i] = min(one, two)
        else:
            b = 'no stone −1'; best[i] = one
        rows.append([str(i), str(h[i]), a, b, str(best[i])])
    assert best[-1] == P.frog_table(h)
    return rows


# ---------------------------------------------------------------- Lesson 2 traces
def dice_sequences(total, faces=range(1, 7)):
    if total == 0:
        return [[]]
    return [s + [f] for f in faces if f <= total for s in dice_sequences(total - f, faces)]


def dice_fill(n, faces=tuple(range(1, 7))):
    ways = [0] * (n + 1); ways[0] = 1
    rows = [['0', 'nothing: the empty sequence', 'start value', '1']]
    for total in range(1, n + 1):
        parts = [total - f for f in faces if total >= f]
        ways[total] = sum(ways[p] for p in parts) % P.MOD
        rows.append([str(total), ' + '.join(f'ways[{p}]' for p in parts), ' + '.join(str(ways[p]) for p in parts), str(ways[total])])
    fn = P.dice_table if tuple(faces) == tuple(range(1, 7)) else P.dice_123
    assert ways[n] == fn(n)
    return rows


def grid_counts(rows):
    n = len(rows); paths = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if rows[r][c] == '*':
                continue
            paths[r][c] = 1 if (r, c) == (0, 0) else (paths[r - 1][c] if r else 0) + (paths[r][c - 1] if c else 0)
    assert paths[-1][-1] == P.grid_table(rows)
    return paths


def grid_fill(rows):
    """Rows (cell, rule, from above, from left, count) in filling order."""
    n = len(rows); paths = grid_counts(rows); out = []
    for r in range(n):
        for c in range(n):
            cell = f'({r}, {c})'
            if rows[r][c] == '*':
                out.append([cell, 'blocked', '—', '—', '0'])
            elif (r, c) == (0, 0):
                out.append([cell, 'open start', '—', '—', '1'])
            else:
                above = f'paths[{r-1}][{c}] = {paths[r-1][c]}' if r else 'outside: 0'
                left = f'paths[{r}][{c-1}] = {paths[r][c-1]}' if c else 'outside: 0'
                out.append([cell, 'open', above, left, f'{(paths[r-1][c] if r else 0)} + {(paths[r][c-1] if c else 0)} = {paths[r][c]}'])
    return out


def grid_routes(rows):
    n = len(rows)
    def walk(r, c):
        if r >= n or c >= n or rows[r][c] == '*':
            return []
        if (r, c) == (n - 1, n - 1):
            return [[]]
        return [['right'] + w for w in walk(r, c + 1)] + [['down'] + w for w in walk(r + 1, c)]
    out = walk(0, 0)
    assert len(out) == P.grid_table(rows)
    return out


def window_trace(n):
    """State of dice_window at the start of each total 1..n+1 (and the slot contents' totals)."""
    recent = [0] * 6; recent[0] = 1; window = 1
    totals = [0, -5, -4, -3, -2, -1]
    states = []
    for total in range(1, n + 2):
        states.append(dict(recent=list(recent), totals=list(totals), window=window))
        if total > n:
            break
        slot = total % 6
        oldest = recent[slot]
        recent[slot] = window; totals[slot] = total
        window = (window - oldest + recent[slot]) % P.MOD
    assert states[-1]['recent'][n % 6] == P.dice_window(n)
    return states


def grid_cells_of(moves):
    r = c = 0; cells = ['(0,0)']
    for m in moves:
        r, c = (r, c + 1) if m == 'right' else (r + 1, c)
        cells.append(f'({r},{c})')
    return cells


# ---------------------------------------------------------------- Lesson 3 traces
def tower_fill(bosses):
    """Rows from i = n down to 0: (i, boss, friend options, friend[i], you options, you[i])."""
    n = len(bosses); friend = [0] * (n + 1); you = [0] * (n + 1)
    rows = [[str(n), '—', 'no bosses left', '0', 'no bosses left', '0']]
    for i in range(n - 1, -1, -1):
        f1 = bosses[i] + you[i + 1]; y1 = friend[i + 1]
        fo = [f'take 1: {bosses[i]} + you[{i+1}] = {bosses[i]} + {you[i+1]} = {f1}']
        yo = [f'take 1: 0 + friend[{i+1}] = {y1}']
        friend[i], you[i] = f1, y1
        if i + 1 < n:
            f2 = bosses[i] + bosses[i + 1] + you[i + 2]; y2 = friend[i + 2]
            fo.append(f'take 2: {bosses[i]} + {bosses[i+1]} + you[{i+2}] = {f2}')
            yo.append(f'take 2: 0 + friend[{i+2}] = {y2}')
            friend[i] = min(f1, f2); you[i] = min(y1, y2)
        rows.append([str(i), str(bosses[i]), ';  '.join(fo), str(friend[i]), ';  '.join(yo), str(you[i])])
    assert friend[0] == P.tower_table(bosses)
    return rows, friend, you


def tower_schedule(bosses):
    """One optimal schedule: [(player, [boss indices])], following the table forward."""
    _, friend, you = tower_fill(bosses)
    n = len(bosses); i = 0; turn = 'friend'; out = []
    while i < n:
        table, other = (friend, you) if turn == 'friend' else (you, friend)
        for take in (2, 1):
            if i + take <= n:
                pay = sum(bosses[i:i + take]) if turn == 'friend' else 0
                if pay + other[i + take] == table[i]:
                    out.append((turn, list(range(i, i + take)))); i += take; break
        turn = 'you' if turn == 'friend' else 'friend'
    assert sum(sum(bosses[j] for j in b) for p, b in out if p == 'friend') == P.tower_table(bosses)
    return out


def array_fillings(values, m):
    from itertools import product
    out = [list(v) for v in product(range(1, m + 1), repeat=len(values))
           if all(values[i] in (0, v[i]) for i in range(len(values))) and all(abs(v[i] - v[i - 1]) <= 1 for i in range(1, len(values)))]
    assert len(out) == P.array_rolling(values, m)
    return out


def array_fill(values, m):
    """Prefix table with arithmetic: rows (position, given, cell for v = 1..m)."""
    table = [[0] * (m + 2) for _ in values]
    rows = []
    for v in range(1, m + 1):
        table[0][v] = 1 if values[0] in (0, v) else 0
    rows.append(['0', str(values[0])] + [('1' if table[0][v] else f'0 (fixed to {values[0]})') for v in range(1, m + 1)])
    for i in range(1, len(values)):
        cells = []
        for v in range(1, m + 1):
            if values[i] in (0, v):
                a, b, c = table[i - 1][v - 1], table[i - 1][v], table[i - 1][v + 1]
                table[i][v] = a + b + c
                cells.append(f'{a} + {b} + {c} = {table[i][v]}')
            else:
                cells.append(f'0 (fixed to {values[i]})')
        rows.append([str(i), str(values[i])] + cells)
    assert sum(table[-1]) == P.array_full(values, m)
    return rows, table


def array_completions(values, m):
    """count(i, previous) for every reachable state, i from n down to 0."""
    n = len(values); memo = {}
    def count(i, prev):
        if i == n:
            return 1
        if (i, prev) not in memo:
            memo[i, prev] = sum(count(i + 1, v) for v in range(1, m + 1)
                                if values[i] in (0, v) and (i == 0 or abs(v - prev) <= 1))
        return memo[i, prev]
    total = count(0, 0)
    assert total == P.array_cached(values, m)
    return memo, total


# ---------------------------------------------------------------- Lesson 4 traces
def feast_layers(limit, a, b):
    """Independent re-computation of the three passes, with every mark recorded."""
    dry = [False] * (limit + 1); wet = [False] * (limit + 1); dry[0] = True
    dry_rows, water_rows, wet_rows = [], [], []
    dry_moves = wet_moves = 0
    for f in range(limit + 1):
        if dry[f]:
            marks = [f + x for x in (a, b) if f + x <= limit]
            for g in marks: dry[g] = True
            dry_moves += len(marks)
            dry_rows.append([str(f), ', '.join(f'{f} + {x} = {f + x}' + ('' if f + x <= limit else ' > limit') for x in (a, b))])
    for f in range(limit + 1):
        if dry[f]:
            wet[f // 2] = True
            water_rows.append([str(f), f'{f} // 2 = {f // 2}'])
    for f in range(limit + 1):
        if wet[f]:
            marks = [f + x for x in (a, b) if f + x <= limit]
            for g in marks: wet[g] = True
            wet_moves += len(marks)
            wet_rows.append([str(f), ', '.join(f'{f} + {x} = {f + x}' + ('' if f + x <= limit else ' > limit') for x in (a, b))])
    best = max(f for f in range(limit + 1) if dry[f] or wet[f])
    assert best == P.feast_table(limit, a, b)
    return dict(dry=dry, wet=wet, dry_rows=dry_rows, water_rows=water_rows, wet_rows=wet_rows,
                D=sum(dry), W=sum(wet), dry_moves=dry_moves, wet_moves=wet_moves, best=best)


def yn(flags):
    return ['Y' if x else '–' for x in flags]


def feast_from(start, limit, a, b):
    """Largest fullness reachable by fruit alone from `start` (no water)."""
    reach = [False] * (limit + 1); reach[start] = True
    for f in range(start, limit + 1):
        if reach[f]:
            for x in (a, b):
                if f + x <= limit: reach[f + x] = True
    return max(f for f in range(limit + 1) if reach[f])


def feast_seeds(limit, a, b):
    L = feast_layers(limit, a, b)
    return [any(L['dry'][d] and d // 2 == f for d in range(limit + 1)) for f in range(limit + 1)]


# ---------------------------------------------------------------- Lesson 5 traces
G = 'HPS'


def hps_fixed(john):
    """Wins for each fixed gesture: rows (gesture, per-round wins, total)."""
    rows = []
    for g in G:
        wins = [int(P.BEATS[g] == x) for x in john]
        rows.append([g, ' + '.join(map(str, wins)), str(sum(wins))])
    assert max(int(r[2]) for r in rows) == P.hps_table(john, 0)
    return rows


def hps_strategies(john, budget):
    """Every strategy using at most `budget` switches, with its wins."""
    from itertools import product
    out = []
    for s in product(G, repeat=len(john)):
        sw = sum(s[i] != s[i - 1] for i in range(1, len(s)))
        if sw <= budget:
            out.append((''.join(s), sw, sum(P.BEATS[a] == b for a, b in zip(s, john))))
    assert max(w for *_, w in out) == P.hps_table(john, budget)
    return out


def hps_best_strategy(john, budget):
    return max(hps_strategies(john, budget), key=lambda x: (x[2], -x[1]))


def hps_layers(john, budget):
    """before-tables after each round (None = impossible) and, for every cell of
    rounds 1.., the worked candidates: (round, john, used, gesture, stay, switch, win, value)."""
    imp = None
    mx = lambda xs: max([x for x in xs if x is not None], default=None)
    before = [[imp] * 3 for _ in range(budget + 1)]
    for g, x in enumerate(G):
        before[0][g] = int(P.BEATS[x] == john[0])
    layers = [before]; work = []
    for r, opp in enumerate(john[1:], 1):
        now = [[imp] * 3 for _ in range(budget + 1)]
        for used in range(budget + 1):
            for g, x in enumerate(G):
                stay = before[used][g]
                sw = [(G[o], before[used - 1][o]) for o in range(3) if o != g] if used > 0 else []
                best = mx([stay] + [v for _, v in sw])
                win = int(P.BEATS[x] == opp)
                now[used][g] = None if best is None else best + win
                fmt = lambda v: '–' if v is None else str(v)
                work.append([str(r), opp, str(used), x, fmt(stay),
                             ', '.join(f'{o}: {fmt(v)}' for o, v in sw) if sw else 'not allowed',
                             str(win), '–' if best is None else f'{best} + {win} = {best + win}'])
        before = now; layers.append(before)
    final = max(v for row in before for v in row if v is not None)
    assert final == P.hps_table(john, budget)
    return layers, work


def hps_prefix_table(john, budget):
    layers, _ = hps_layers(john, budget)
    rows = []
    for r, layer in enumerate(layers):
        rows.append([john[:r + 1]] + ['–' if v is None else str(v) for used in range(budget + 1) for v in layer[used]])
    return rows
