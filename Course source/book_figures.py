"""TikZ figures for the tutor books, in the course style (charcoal lines, grey wash).

Geometry and labels are computed from programs.py so a figure cannot disagree with
the code. Each function returns the body of a tikzpicture (without the environment).
"""
import programs as P
import book_kit as K
from build_course import esc

STYLE = (r'>=Stealth,every node/.style={font=\small},'
         r'box/.style={draw=ink,rounded corners=2pt,minimum height=7mm,fill=paper,inner sep=3pt},'
         r'arr/.style={->,thick,ink},thin arr/.style={->,ink},'
         r'call/.style={circle,draw=ink,minimum size=6.4mm,inner sep=0pt,font=\ttfamily\footnotesize},'
         r'repeat/.style={call,fill=wash,draw=quiet,dashed},'
         r'cell/.style={draw=ink,minimum size=9mm,inner sep=0pt},'
         r'note/.style={font=\footnotesize,text=quiet}')


def picture(body, scale=None):
    opts = STYLE + (f',scale={scale},every node/.append style={{transform shape}}' if scale else '')
    return r'\begin{tikzpicture}[' + opts + ']' + body + r'\end{tikzpicture}'


# ---------------------------------------------------------------- Lesson 1
def call_tree(root, children, count_check, dx=0.98, dy=1.05, scale=0.92):
    """Complete call tree: children(k) lists the arguments of the calls made by call k.
    Calls repeating an argument already asked earlier (Python's calling order) are shaded."""
    nodes, edges, seen = [], [], set()
    leaf = [0]
    def visit(k, depth):
        me = len(nodes); nodes.append(None)
        repeated = k in seen; seen.add(k)
        kids = children(k)
        if not kids:
            x = leaf[0]; leaf[0] += 1
        else:
            ids = [visit(c, depth + 1) for c in kids]
            for c in ids: edges.append((me, c))
            x = (nodes[ids[0]][0] + nodes[ids[-1]][0]) / 2
        nodes[me] = (x, depth, k, repeated)
        return me
    visit(root, 0)
    assert len(nodes) == count_check
    body = ''
    for i, (x, d, k, rep) in enumerate(nodes):
        body += rf'\node[{"repeat" if rep else "call"}] (n{i}) at ({x*dx:.2f},{-d*dy:.2f}) {{{k}}};'
    for a, b in edges:
        body += rf'\draw[ink] (n{a})--(n{b});'
    low = -(max(d for _, d, _, _ in nodes) + 1) * dy
    body += rf'\node[call] at (0,{low:.2f}) {{k}};\node[anchor=west,note] at (0.4,{low:.2f}) {{first call with this argument}};'
    body += rf'\node[repeat] at (5.2,{low:.2f}) {{k}};\node[anchor=west,note] at (5.6,{low:.2f}) {{repeats an earlier question}};'
    shaded = sum(rep for *_, rep in nodes)
    return picture(body, scale=scale), len(nodes), shaded, len({k for *_, k, _ in nodes})


def stairs_call_tree(n=5):
    """The complete call tree of stairs_slow(n)."""
    return call_tree(n, lambda k: [k - 1, k - 2] if k > 0 else [], K.calls(P.stairs_slow, (n,)))


def call_stack(n=5):
    line = K.listing_line('stairs_cached', 'cache[step] = ways(')
    top = K.listing_line('stairs_cached', 'return ways(n)')
    frames = [f'stairs_cached({n})  paused at line {top}, waiting for ways({n})']
    frames += [f'ways({k})  paused at line {line}, waiting for ways({k-1})' for k in range(n, 0, -1)]
    frames += ['ways(0)  found in the cache: returns 1 at once']
    body = ''
    for i, text in enumerate(frames):
        fill = 'wash' if i == len(frames) - 1 else 'paper'
        body += rf'\node[box,fill={fill},minimum width=88mm,anchor=south west,font=\ttfamily\footnotesize] at (0,{i*0.82:.2f}) {{{esc(text)}}};'
    h = len(frames) * 0.82
    body += rf'\draw[arr] (9.4,0.1)--node[right,note,align=left]{{newest frame\\on top}}(9.4,{h-0.2:.2f});'
    body += rf'\node[note,anchor=north west,text width=88mm] at (0,-0.15) {{Oldest frame at the bottom. Each line of text is one stack frame: a call that has started and not yet returned.}};'
    return picture(body), len(frames)


def frog_routes(heights=(20, 50, 30, 40, 10, 10)):
    """Stones drawn as columns; best route above (solid), greedy route below (dashed)."""
    best_route, best_cost = K.frog_best_route(list(heights))
    greedy_route, greedy_cost = K.frog_greedy(list(heights))
    gap, w, scale = 2.0, 0.9, 1.8 / max(heights)
    body = ''
    for i, h in enumerate(heights):
        x = i * gap
        body += rf'\draw[ink,fill=wash] ({x-w/2:.2f},0) rectangle ({x+w/2:.2f},{h*scale:.2f});'
        body += rf'\node[font=\footnotesize] at ({x:.2f},{h*scale+0.22:.2f}) {{{h}}};'
        body += rf'\node[note] at ({x:.2f},-0.3) {{stone {i}}};'
    top = max(heights) * scale + 0.55
    for a, b in zip(best_route, best_route[1:]):
        cost = abs(heights[b] - heights[a])
        body += rf'\draw[arr,line width=1.3pt] ({a*gap:.2f},{top:.2f}) to[bend left=38] node[above,font=\footnotesize]{{{cost}}} ({b*gap:.2f},{top:.2f});'
    for a, b in zip(greedy_route, greedy_route[1:]):
        cost = abs(heights[b] - heights[a])
        body += rf'\draw[arr,dashed,quiet] ({a*gap:.2f},-0.6) to[bend right=38] node[below,font=\footnotesize]{{{cost}}} ({b*gap:.2f},-0.6);'
    end = (len(heights) - 1) * gap
    legend_x = end + 1.2
    body += rf'\draw[arr,line width=1.3pt] ({legend_x:.2f},{top:.2f})--++(0.8,0) node[right,font=\footnotesize,align=left] {{best route {"-".join(map(str,best_route))}\\total {best_cost}}};'
    body += rf'\draw[arr,dashed,quiet] ({legend_x:.2f},-0.9)--++(0.8,0) node[right,font=\footnotesize,align=left,text=ink] {{greedy route {"-".join(map(str,greedy_route))}\\total {greedy_cost}}};'
    return picture(body, scale=0.78), best_route, best_cost, greedy_route, greedy_cost


# ---------------------------------------------------------------- Lesson 2
def dice_call_tree(n=4):
    return call_tree(n, lambda k: [k - f for f in range(1, min(6, k) + 1)], K.calls(P.dice_slow, (n,)), dx=0.9)


def grid_counts(rows, highlight=None, size=1.25):
    """The grid with its blocked cells, the path count in every open cell and an
    arrow from above and from the left into every open cell that receives one."""
    n = len(rows)
    paths = K.grid_counts(rows)
    body = ''
    for r in range(n):
        for c in range(n):
            x, y = c * size, -r * size
            blocked = rows[r][c] == '*'
            body += rf'\draw[ink,fill={"lightink" if blocked else "paper"}] ({x:.2f},{y:.2f}) rectangle ({x+size:.2f},{y-size:.2f});'
            body += rf'\node[anchor=north west,inner sep=2pt,font=\scriptsize,text=quiet] at ({x:.2f},{y:.2f}) {{{r},{c}}};'
            label = r'\footnotesize blocked' if blocked else rf'\large {paths[r][c]}'
            body += rf'\node at ({x+size/2:.2f},{y-size/2-0.08:.2f}) {{{label}}};'
    for r in range(n):
        for c in range(n):
            if rows[r][c] == '*' or (r, c) == (0, 0):
                continue
            x, y = c * size + size / 2, -r * size - size / 2
            strong = (r, c) == highlight
            style = 'arr,line width=1.2pt' if strong else 'thin arr,quiet'
            if r > 0:
                body += rf'\draw[{style}] ({x+0.28:.2f},{y+size-0.32:.2f})--({x+0.28:.2f},{y+0.28:.2f});'
            if c > 0:
                body += rf'\draw[{style}] ({x-size+0.32:.2f},{y-0.28:.2f})--({x-0.3:.2f},{y-0.28:.2f});'
    body += rf'\node[anchor=south west,note] at (0,0.05) {{start (0,0)}};\node[anchor=north east,note] at ({n*size:.2f},{-n*size-0.05:.2f}) {{finish ({n-1},{n-1})}};'
    return picture(body)


def window_slots():
    """dice_window just before and just after it handles total 7."""
    rows = K.window_trace(8)
    before, after = rows[6], rows[7]          # states entering total 7 and total 8
    body = ''
    for row, (label, state) in enumerate([('before total 7', before), ('after total 7', after)]):
        y = -row * 1.55
        body += rf'\node[anchor=east,font=\footnotesize] at (-0.2,{y-0.45:.2f}) {{{label}}};'
        for slot in range(6):
            x = slot * 1.75
            changed = slot == 7 % 6
            body += rf'\draw[ink,fill={"wash" if changed else "paper"}] ({x:.2f},{y:.2f}) rectangle ({x+1.6:.2f},{y-0.9:.2f});'
            body += rf'\node[font=\footnotesize] at ({x+0.8:.2f},{y-0.3:.2f}) {{{state["recent"][slot]}}};'
            body += rf'\node[note] at ({x+0.8:.2f},{y-0.68:.2f}) {{total {state["totals"][slot]}}};'
        body += rf'\node[anchor=west,font=\footnotesize] at ({6*1.75:.2f},{y-0.45:.2f}) {{window = {state["window"]}}};'
    for slot in range(6):
        body += rf'\node[note] at ({slot*1.75+0.8:.2f},0.25) {{slot {slot}}};'
    body += rf'\draw[arr] ({1*1.75+0.8:.2f},-0.95)--({1*1.75+0.8:.2f},-1.5);'
    return picture(body, scale=0.8)


# ---------------------------------------------------------------- Lesson 3
def boss_strip(bosses):
    """Bosses in order; shaded = defeated by the friend, white = defeated by you.
    A brace under each turn names the player and the points paid."""
    sched = K.tower_schedule(bosses)
    w = 1.15
    body = ''
    for player, idx in sched:
        for j in idx:
            x = j * w
            fill = 'lightink' if player == 'friend' else 'paper'
            body += rf'\draw[ink,fill={fill}] ({x:.2f},0) rectangle ({x+w-0.1:.2f},1);'
            body += rf'\node at ({x+(w-0.1)/2:.2f},0.55) {{\large {bosses[j]}}};'
            body += rf'\node[note] at ({x+(w-0.1)/2:.2f},1.25) {{boss {j}}};'
        a, b = idx[0] * w, idx[-1] * w + w - 0.1
        paid = sum(bosses[j] for j in idx) if player == 'friend' else 0
        body += rf'\draw[ink] ({a:.2f},-0.15)--({a:.2f},-0.3)--({b:.2f},-0.3)--({b:.2f},-0.15);'
        body += rf'\node[font=\footnotesize,align=center] at ({(a+b)/2:.2f},-0.75) {{{player}\\pays {paid}}};'
    return picture(body)


def tower_dependencies(bosses, at=1):
    """Two rows friend[i] and you[i]; arrows show which later entries entry `at` reads."""
    _, friend, you = K.tower_fill(bosses)
    n = len(bosses); w = 1.6
    body = ''
    for row, (name, vals) in enumerate([('friend', friend), ('you', you)]):
        y = -row * 1.9
        body += rf'\node[anchor=east,font=\ttfamily\footnotesize] at (-0.75,{y:.2f}) {{{name}[i]}};'
        for i in range(n + 1):
            fill = 'wash' if i == at else 'paper'
            body += rf'\node[cell,fill={fill},minimum width=12mm,minimum height=8mm] ({name}{i}) at ({i*w:.2f},{y:.2f}) {{{vals[i]}}};'
    for i in range(n + 1):
        body += rf'\node[note] at ({i*w:.2f},0.75) {{i = {i}}};'
    for d in (1, 2):
        if at + d <= n:
            body += rf'\draw[arr,shorten >=2pt,shorten <=2pt] (you{at+d}.north) -- ([xshift=-2mm]friend{at}.south);'
            body += rf'\draw[arr,dashed,quiet,shorten >=2pt,shorten <=2pt] (friend{at+d}.south) -- ([xshift=2mm]you{at}.north);'
    body += rf'\node[note,anchor=north west,text width=110mm] at (-1.6,-2.6) {{Solid arrows: friend[{at}] reads you[{at+1}] and you[{at+2}] (the friend takes 1 or 2 bosses, then you move). Dashed: you[{at}] reads friend[{at+1}] and friend[{at+2}]. Every arrow points from a larger i to a smaller one, so the table is filled from i = {n} down to 0.}};'
    return picture(body, scale=0.95)


def array_dependencies(values, m, row, v):
    """Rows 0..n−1 by columns 0..m+1 (padding greyed); arrows from row−1, columns
    v−1, v, v+1 into [row][v]."""
    _, table = K.array_fill(values, m)
    w, h = 1.35, 0.85
    body = ''
    for c in range(m + 2):
        label = 'pad' if c in (0, m + 1) else f'v = {c}'
        body += rf'\node[note] at ({c*w:.2f},0.6) {{{label}}};'
    for i in range(len(values)):
        y = -i * h * 1.25
        body += rf'\node[anchor=east,font=\footnotesize] at ({-0.8:.2f},{y:.2f}) {{position {i} (given {values[i]})}};'
        for c in range(m + 2):
            pad = c in (0, m + 1)
            fill = 'lightink' if pad else ('wash' if (i, c) == (row, v) else 'paper')
            body += rf'\node[cell,fill={fill},minimum width=11mm,minimum height=7mm] (t{i}x{c}) at ({c*w:.2f},{y:.2f}) {{{table[i][c]}}};'
    for c in (v - 1, v, v + 1):
        body += rf'\draw[arr,shorten >=1pt,shorten <=1pt] (t{row-1}x{c}.south)--(t{row}x{v}.north);'
    return picture(body, scale=0.9)


def overwrite_picture(prev=(1, 1, 1)):
    """A correct new row built from an untouched old row, and the same row updated in place."""
    m = len(prev)
    old = [0] + list(prev) + [0]
    good = [old[v - 1] + old[v] + old[v + 1] for v in range(1, m + 1)]
    bad = old[:]
    steps = []
    for v in range(1, m + 1):
        bad[v] = bad[v - 1] + bad[v] + bad[v + 1]
        steps.append(bad[v])
    w = 1.4
    body = ''
    def row(y, label, vals, fill='paper'):
        out = rf'\node[anchor=east,font=\footnotesize] at (-0.75,{y:.2f}) {{{label}}};'
        for k, x in enumerate(vals):
            out += rf'\node[cell,fill={fill},minimum width=12mm,minimum height=7mm] at ({k*w:.2f},{y:.2f}) {{{x}}};'
        return out
    body += rf'\node[anchor=west,font=\footnotesize\heavy] at (-3.2,1.0) {{Two rows (correct)}};'
    body += row(0, 'before', prev) + row(-1.0, 'now', good, 'wash')
    x0 = 6.8
    body += rf'\node[anchor=west,font=\footnotesize\heavy] at ({x0-1.0:.2f},1.0) {{One row updated in place (wrong)}};'
    for k, x in enumerate(prev):
        body += rf'\node[cell,minimum width=12mm,minimum height=7mm] at ({x0+1.5+k*w:.2f},0) {{{x}}};'
        body += rf'\node[cell,fill=lightink,minimum width=12mm,minimum height=7mm] at ({x0+1.5+k*w:.2f},-1.0) {{{steps[k]}}};'
    body += rf'\node[anchor=east,font=\footnotesize] at ({x0+0.55:.2f},0) {{start}};\node[anchor=east,font=\footnotesize] at ({x0+0.55:.2f},-1.0) {{after}};'
    body += rf'\node[note,anchor=north west,text width=120mm] at (-3.2,-1.7) {{With two rows each new count reads three untouched old counts: {", ".join(str(g) for g in good)}. In place, the count for v = 2 reads the new {steps[0]} already written for v = 1, giving {steps[1]} instead of {good[1]}, and the error spreads to v = 3.}};'
    return picture(body, scale=0.85), good, steps


# ---------------------------------------------------------------- Lesson 4
def feast_layers(limit=10, a=4, b=7, route=((0, 'dry'), (7, 'dry'), (3, 'wet'), (10, 'wet'))):
    """Dry layer above, wet layer below. Fruit arrows stay in a layer and point right;
    water arrows go from dry f down-left to wet f // 2. The highlighted route is drawn thick."""
    L = K.feast_layers(limit, a, b)
    w, gap = 1.12, 2.6
    body = ''
    for name, y in (('dry', 0), ('wet', -gap)):
        body += rf'\node[anchor=east,font=\footnotesize] at (-0.7,{y:.2f}) {{{name}}};'
        for f in range(limit + 1):
            on = L[name][f]
            body += rf'\node[cell,minimum size=8mm,fill={"wash" if on else "paper"},text={"ink" if on else "lightink"}] ({name}{f}) at ({f*w:.2f},{y:.2f}) {{{f}}};'
    hot = set()
    for (f, layer), (g, layer2) in zip(route, route[1:]):
        hot.add((f, layer, g, layer2))
    def edge(f, l1, g, l2, kind):
        strong = (f, l1, g, l2) in hot
        style = 'arr,line width=1.3pt' if strong else 'thin arr,lightink'
        if kind == 'fruit':
            side = 'north' if l1 == 'dry' else 'south'
            bend = 'bend left=35' if l1 == 'dry' else 'bend right=35'
            return rf'\draw[{style}] ({l1}{f}.{side}) to[{bend}] ({l2}{g}.{side});'
        return rf'\draw[{style}] ({l1}{f}.south) -- ({l2}{g}.north);'
    for layer in ('dry', 'wet'):
        for f in range(limit + 1):
            if L[layer][f]:
                for x in (a, b):
                    if f + x <= limit:
                        body += edge(f, layer, f + x, layer, 'fruit')
    for f in range(limit + 1):
        if L['dry'][f]:
            body += edge(f, 'dry', f // 2, 'wet', 'water')
    body += rf'\node[note,anchor=north west,text width=125mm] at (-1.4,{-gap-2.1:.2f}) {{Shaded cells are reachable. Curved arrows: eat a fruit ({a} or {b}), staying in the layer. Straight arrows: drink, from dry f to wet f // 2. Thick: the route 0 → 7 → 3 → 10.}};'.replace('→', r'{\ttfamily →}')
    return picture(body, scale=0.92)


# ---------------------------------------------------------------- Lesson 5
def hps_transition(john='HHSSP', rnd=2, used=1, g='H'):
    """The two before rows (used − 1 and used) after round rnd − 1, with arrows
    into now[used][g] for round rnd: stay from before[used][g], switch from the other
    gestures of row used − 1."""
    layers, _ = K.hps_layers(john, used)
    before = layers[rnd - 1]
    gi = K.G.index(g)
    win = int(P.BEATS[g] == john[rnd])
    cands = [before[used][gi]] + [before[used - 1][o] for o in range(3) if o != gi]
    best = max(v for v in cands if v is not None)
    value = best + win
    assert value == layers[rnd][used][gi]
    w = 1.5
    body = ''
    for row, u in enumerate((used - 1, used)):
        y = -row * 1.6
        body += rf'\node[anchor=east,font=\footnotesize] at (-0.9,{y:.2f}) {{before[{u}]}};'
        for k, x in enumerate(K.G):
            v = before[u][k]
            used_cell = (u == used and x == g) or (u == used - 1 and x != g)
            body += rf'\node[cell,minimum width=13mm,minimum height=8mm,fill={"wash" if used_cell else "paper"},text={"ink" if used_cell else "quiet"}] (b{u}{x}) at ({k*w:.2f},{y:.2f}) {{{x}: {"–" if v is None else v}}};'
    body += rf'\node[cell,fill=wash,minimum width=28mm,minimum height=9mm,line width=1pt] (t) at (7.6,-0.8) {{now[{used}][{g}] = {value}}};'
    others = [x for x in K.G if x != g]
    near, far = others[-1], others[0]
    body += rf'\draw[arr,dashed] (b{used-1}{near}.east) to[out=0,in=150] (t.north west);'
    body += rf'\draw[arr,dashed] (b{used-1}{far}.north) to[out=50,in=120] node[pos=0.5,above,font=\scriptsize] {{switch: one more switch, other gesture}} (t.north);'
    body += rf'\draw[arr] (b{used}{g}.south) to[out=-50,in=-120] node[pos=0.5,below,font=\scriptsize] {{stay: same switches, same gesture}} (t.south);'
    stay = before[used][gi]; sw = [before[used - 1][o] for o in range(3) if o != gi]
    body += rf'\node[note,anchor=north west,text width=125mm] at (-2.4,-4.0) {{Round {rnd} (John plays {john[rnd]}). Stay: before[{used}][{g}] = {stay}. Switch from the other gestures with {used - 1} switch{"es" if used - 1 != 1 else ""} used: {", ".join(map(str, sw))}. Best = {best}; {g} beats {john[rnd]}, so add {win}: {best} + {win} = {value}.}};'
    return picture(body), value
