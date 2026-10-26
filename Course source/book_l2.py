"""Lesson 2 tutor book: Dice Combinations and Grid Paths. Main idea: count the ways to arrive."""
import inspect
import programs as P
import book_kit as K
import book_figures as F
from book_blocks import (section, chapter, code, diagram, table, pause, figure, python,
                         problem, items, recap, listing, judge, cost, edges, mistakes)

C = K.comma
G3 = ['...', '.*.', '...']
G4 = ['....', '..*.', '*...', '....']
TREE, TREE_CALLS, TREE_REPEATS, TREE_DISTINCT = F.dice_call_tree(4)
DICE_CALLS = [(n, K.calls(P.dice_slow, (n,)), K.calls(P.dice_cached, (n,), 'count')) for n in (4, 6, 10, 20)]
T_DICE = K.seconds(P.dice_table, (10 ** 6,))
T_GRID = K.seconds(P.grid_table, (['.' * 1000] * 1000,))
SEQ4 = K.dice_sequences(4)
seq = lambda s: ''.join(map(str, s))

dice_problem = problem(
    name='Dice Combinations',
    story='How many ways can throws of an ordinary die add up to exactly n?',
    rules='Build an ordered list using the numbers 1, 2, 3, 4, 5 and 6, as many times as you like, with any positive length. Count the lists whose sum is exactly n. Order matters: 1 then 2 is a different list from 2 then 1. Each list stands for one sequence of die throws; we count sequences, we do not simulate throws or compute probabilities.',
    input='one line holding n.',
    output='the number of lists, as its remainder after dividing by 1,000,000,007.',
    limits='1 ≤ n ≤ 1,000,000. The judge allows 1 second and 512 MB.',
    example_in='3', example_out=str(P.dice_table(3)),
    why='The four lists are 111, 12, 21 and 3. A list containing 4, 5 or 6 already exceeds 3.',
    source='CSES Problem Set, task 1633.', url='https://cses.fi/problemset/task/1633')

grid_problem = problem(
    name='Grid Paths',
    story='Cross a square grid from corner to corner, moving only right or down.',
    rules='A grid has n rows and n columns. Each cell is open, written . (a dot), or blocked, written * (a star). Start on the top-left cell and finish on the bottom-right cell. Each move goes one cell right or one cell down, and a path may never enter a blocked cell. If the start or the finish is blocked there are no paths. Count the paths.',
    input='the first line holds n; then n lines of n characters, the rows from top to bottom.',
    output='the number of paths, as its remainder after dividing by 1,000,000,007.',
    limits='1 ≤ n ≤ 1,000. The judge allows 1 second and 512 MB.',
    example_in='4\n' + '\n'.join(G4), example_out=str(P.grid_table(G4)),
    why=f'There are {len(K.grid_routes(G4))} paths around the two blocked cells; section 2.6 finds them with a count table.',
    source='CSES Problem Set, task 1638.', url='https://cses.fi/problemset/task/1638')

DICE_TABLE_SRC = inspect.getsource(P.dice_table)
GRID_SRC = inspect.getsource(P.grid_table)
GRID_START_FIRST = GRID_SRC.replace("""            if rows[r][c] == '*':
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:""", """            if r == 0 and c == 0:
                paths[r][c] = 1
            elif rows[r][c] == '*':
                continue
            else:""")
assert GRID_START_FIRST != GRID_SRC

ch1 = chapter('Dice: count sequences with an exact total', 'Turn a story about dice into a precise counting question and solve it three ways.',
section('The Dice Combinations problem', ['L2-01', 'L2-02'], 'State the problem exactly and connect it to the staircase of Lesson 1.', 'List the sequences for small totals by hand.',
'''This lesson has one main idea: count the ways to arrive. To count the objects that end at a target, group them by how they arrive, that is by their last move, and add the group sizes. Lesson 1's staircase did exactly this with two possible last jumps; here there are six.''',
dice_problem,
'''Recall from Lesson 1: in staircase, `ways[4] = 5` means there are five routes to step 4; in Frog, `best[4] = 30` means the cheapest route to stone 4 costs 30 (heights 20, 50, 30, 40, 10, 10). Staircase added the counts of disjoint groups; Frog took a minimum of competing costs. Dice is a counting problem, so we will add.'''),
section('What the problem asks us to count', ['L2-02'], 'Enumerate every sequence for totals 1 to 4 and see what "ordered" means.', 'Group the sequences by their last face.',
'''A sequence may use the same value repeatedly, and its length is not fixed. For target 3 the valid sequences are 3, 12, 21 and 111 (we write [1, 2] as 12). A face of 6 is a possible die result, but it cannot appear in a sequence totalling 3: all values are positive, so the total could never come back down.''',
table(['Total', 'Sequences (12 means [1, 2])', 'Count'], [[str(t), ', '.join(seq(s) for s in sorted(K.dice_sequences(t), key=lambda s: (-len(s), s))), str(len(K.dice_sequences(t)))] for t in range(1, 5)], r'>{\raggedright\arraybackslash}p{14mm}X>{\raggedright\arraybackslash}p{12mm}'),
'''For target 0 we use one empty sequence. It supplies the starting contribution for a sequence of a single face: [3] is the empty sequence followed by 3. The empty sequence has length 0 and sum 0, and there is exactly one of it, so the count for total 0 is 1.''',
pause('List the sequences totalling 4. Why is [2, 2] counted once, while [1, 3] and [3, 1] are different?', 'The eight sequences are ' + ', '.join(seq(s) for s in sorted(SEQ4, key=lambda s: (-len(s), s))) + '. Swapping identical 2s does not create a different ordered list; swapping 1 and 3 does.')),
section('Remove the last face', ['L2-03'], 'Derive ways[total] = sum of ways[total − face] over the faces that fit, and fill totals 0 to 7.', 'Write the recurrence as a recursive program and count its calls.',
'''Let `ways[total]` be the number of valid sequences whose sum is total. Take a completed sequence whose last value is face. Removing that value leaves a valid sequence with sum total − face. Conversely, appending face to any sequence with that smaller sum gives a valid sequence with the required total. Sequences with different last faces are different, so the groups do not overlap, and every sequence has some last face, so together they cover everything:''',
table(['Last face', 'Earlier total', 'Sequences with total 4 in this group'], [[str(f), str(4 - f), ', '.join(seq(s) for s in SEQ4 if s[-1] == f) + f'  ({sum(1 for s in SEQ4 if s[-1] == f)})'] for f in range(1, 5)] + [['5, 6', 'negative', 'none: the face is larger than 4']], r'>{\raggedright\arraybackslash}p{16mm}>{\raggedright\arraybackslash}p{20mm}X'),
'''So ways[4] = ways[3] + ways[2] + ways[1] + ways[0] = 4 + 2 + 1 + 1 = 8. The same rule fills every total in order; each line uses only answers already in the table.''',
table(['Total', 'Reads', 'Arithmetic', 'ways[total]'], K.dice_fill(7), r'>{\raggedright\arraybackslash}p{12mm}X>{\raggedright\arraybackslash}p{30mm}>{\raggedright\arraybackslash}p{18mm}'),
'''For total 7 all six faces fit for the first time. The numbers we add are counts of earlier sequences, not the earlier totals themselves.'''),
section('Recursion, and the repeated questions', ['L2-04'], 'Write the direct recursive count, see its repeated calls and measure how fast they grow.', 'Learn the remainder rule the judge needs, before caching.',
'''The direct recursive function asks about each smaller total that a fitting face leaves, and adds the answers. Its stopping value is 1 when the total is 0. The loop chooses only faces that fit, so it never asks about a negative total and needs no negative case.''',
code('dice_slow', 'print(dice_slow(4))'),
python(['sum', 'genexp', 'range', 'min'], 'sum over a generator; range with min', '''`range(1, min(6, n) + 1)` is the faces 1 up to 6, or up to n when n is smaller: those are the faces that fit. `dice_slow(n - face) for face in …` inside `sum(…)` is a generator expression: it produces one count per face, and `sum` adds them. It is a compact way to write a loop that adds into a running total.'''),
figure(TREE, f'The complete call tree of dice_slow(4): {TREE_CALLS} calls but only {TREE_DISTINCT} different totals (0 to 4). The {TREE_REPEATS} shaded calls repeat a total that was already asked.'),
table(['Total n', 'Calls of dice_slow(n)', 'Calls in dice_cached(n)'], [[str(n), C(a), C(b)] for n, a, b in DICE_CALLS]),
f'''Each call with total t makes min(6, t) more calls, so for totals up to 6 the number of calls doubles with each step (2ⁿ calls: {DICE_CALLS[0][1]} for n = 4) and keeps growing exponentially after that: {C(DICE_CALLS[-1][1])} calls for n = 20. A call for target 7 asks about target 5 directly, but target 6 also asks about 5, and so on down many branches.'''),
section('Why remainders can be taken during the calculation', ['L2-06'], 'Explain what "modulo 1,000,000,007" means and why reducing after every addition gives the same final answer.', 'Use the remainder in a cached and an iterative program.',
'''The count grows quickly: ways[n] roughly doubles with each total, so ways[1000] already has hundreds of digits. The judge therefore asks for the remainder after dividing the count by 1,000,000,007. A remainder is not a probability, and it does not count only some of the sequences. It is the representation of the complete count that the problem requests. In Python, `a % m` is the remainder of a divided by m: `11 % 7` is 4.

Use divisor 7 for a small example. Suppose two groups contribute 12 and 13 sequences. Together they contribute 25, whose remainder is 4. Reducing first gives 12 % 7 = 5 and 13 % 7 = 6, and (5 + 6) % 7 = 11 % 7 = 4 as well. Removing whole multiples of 7 never changes a remainder modulo 7.''',
table(['Step', 'Exact total', 'Remainder kept'], [['start', '0', '0'], ['add 5', '5', '(0 + 5) % 7 = 5'], ['add 6', '11', '(5 + 6) % 7 = 4'], ['add 9', '20', '(4 + 9) % 7 = 6'], ['check', '20 % 7 = 6', 'the same 6']]),
'''For addition we can therefore reduce after every update, as long as we use the same divisor throughout. That keeps every stored number below 1,000,000,007 instead of growing to hundreds of thousands of digits. That the divisor is prime is not needed for this addition-only recurrence. In the programs, `MOD` names the divisor; small counts such as 8 and 63 are below it and are unchanged.''',
pause('Under divisor 7, combine counts 5, 6 and 9 by taking a remainder after each addition.', 'After the first two counts: (5 + 6) % 7 = 4. Then (4 + 9) % 7 = 6. This agrees with (5 + 6 + 9) % 7 = 20 % 7 = 6.')),
section('Cache each total', ['L2-04'], 'Save the count for each total in a dictionary and count the calls that remain.', 'Fill the totals in increasing order with a loop.',
'''Saving the count for each total avoids recomputing it. As in staircase, the key is the target total and the stored value is its count of sequences, now kept as a remainder.''',
code('dice_cached', 'print(dice_cached(7))'),
python(['nested', 'dict', 'mod'], 'a nested function, a dictionary and %', '''`count` is defined inside `dice_cached`, so it can read `cache` and `n` from the enclosing function, and a fresh dictionary is created for every top-level call. `cache = {0: 1}` stores the answer for total 0. `total not in cache` tests whether a key is missing. `% MOD` takes the remainder after division by MOD = 1,000,000,007 (line 1 of the listing).'''),
cost('Cost of dice_cached, line by line', 'dice_cached', ((20,), dict(n=20), 'Runs for n = 20'), (dict(n=1000), 'For n = 1,000'),
     [('if total not in cache:', 'once per call of count: 1 + min(6, t) summed over t = 1 to n', lambda n: 1 + sum(min(6, t) for t in range(1, n + 1))),
      ('return cache[total]', 'once per call of count', lambda n: 1 + sum(min(6, t) for t in range(1, n + 1)))]),
'''Each total is solved once with at most six contributions: O(6n), written O(n) because six does not grow with n, and O(n) stored answers. A chain that keeps choosing face 1 is still n calls deep, so the cached version stops with RecursionError long before n = 1,000,000. Caching removes repeated work but not deep recursion.'''),
section('Fill totals in increasing order', ['L2-05'], 'Write the iterative program, give its cost line by line, and run it on a million.', 'Change the set of allowed faces.',
'''Use `ways[total]` for the count of a particular total. Start with `ways[0] = 1`; every other entry starts at 0 because no contributions have been added yet. The outer loop visits totals 1 to n; the inner loop considers the possible last faces. When the loop reaches total 7, totals 1 to 6 are complete, exactly as in the table of section 1.3.''',
code('dice_table', 'print(dice_table(7))'),
python(['listmul', 'augassign', 'modassign'], 'the table and %=', '''`[0] * (n + 1)` is a list of n + 1 zeros, indices 0 to n. `ways[total] += x` adds x to the entry. `ways[total] %= MOD` replaces the entry by its remainder, keeping it small. The check `total >= face` matters because `ways[-1]` would silently read the last entry of the list, not a count for a negative total.'''),
cost('Cost of dice_table, line by line', 'dice_table', ((7,), dict(n=7), 'Runs for n = 7'), (dict(n=10 ** 6), 'For n = 1,000,000'),
     [('for total in range(1, n + 1):', 'n times, plus the final check', lambda n: n + 1),
      ('if total >= face:', 'six times per total', lambda n: 6 * n),
      ('ways[total] += ways[total - face]', 'once per face that fits', lambda n: sum(min(6, t) for t in range(1, n + 1))),
      ('ways[total] %= MOD', 'once per total', lambda n: n)]),
f'''About six million cheap steps for the largest input: O(n) time and O(n) memory, with no recursion. On a recent laptop `dice_table(1000000)` took {T_DICE:.1f} s with CPython.'''),
section('Change the set of allowed faces', ['L2-07'], 'Adapt the recurrence to faces 1, 2 and 3 and check it against an enumeration.', 'Collect the dice edge cases, mistakes and the judge submission.',
'''If only 1, 2 and 3 are allowed, the grouping argument stays the same: the earlier total is one, two or three below the target. The starting entry remains 1, because there is still one empty sequence.''',
table(['Total', 'Reads', 'Arithmetic', 'ways[total]'], K.dice_fill(5, (1, 2, 3)), r'>{\raggedright\arraybackslash}p{12mm}X>{\raggedright\arraybackslash}p{30mm}>{\raggedright\arraybackslash}p{18mm}'),
f'''Total 4 is a useful check: the six-face count 8 included the sequence [4], which is now forbidden, so the answer drops to {P.dice_123(4)}.''',
code('dice_123', 'print([dice_123(n) for n in range(6)])'),
python(['tuple', 'listcomp'], 'a tuple of faces; a list of answers', '''`for face in (1, 2, 3):` lists the allowed faces explicitly, which is clearer than changing the 7 in `range(1, 7)`. The test line `[dice_123(n) for n in range(6)]` is a list comprehension that collects the answers for totals 0 to 5.''')),
section('Dice: edge cases, mistakes and the judge', [], 'Prepare students to test Dice properly and to submit it to CSES.', 'Optionally reduce Dice memory to six entries, then move to Grid Paths.',
edges([['n = 1', '1', 'Only face 1 fits; a program without the `total >= face` check crashes here.'],
       ['n = 6', str(P.dice_table(6)), 'Last total where every face up to the total fits; counts are powers of two so far.'],
       ['n = 7', str(P.dice_table(7)), 'First total above the largest face; 32 + 16 + 8 + 4 + 2 + 1.'],
       ['n = 1,000,000', C(P.dice_table(10 ** 6)), 'Needs the remainder at every step and a loop, not recursion.']]),
mistakes([['`ways[0] = 0`', 'loses the empty sequence', K.variant('dice_table', 'ways[0] = 1', 'ways[0] = 0', 'dice_table(7)') + ' (63)'],
          ['no `total >= face` check', 'reads ways[−1], ways[−2], … at the end of the list', K.variant('dice_table', 'if total >= face:', 'if True:', 'dice_table(1)') + ' for n = 1; ' + K.variant('dice_table', 'if total >= face:', 'if True:', 'dice_table(4)') + ' for n = 4 (8)'],
          ['`range(1, 6)` for the faces', 'forgets face 6', K.variant('dice_table', 'range(1, 7)', 'range(1, 6)', 'dice_table(7)') + ' (63)'],
          ['`MOD = 1e9 + 7`', '1e9 is a float, so every count becomes a float', K.run_variant(DICE_TABLE_SRC.replace('MOD', '(1e9 + 7)'), 'dice_table(7)') + ' (63): the judge rejects it'],
          ['dice_cached on n = 5,000', 'the chain of calls is 5,000 deep', K.variant('dice_cached', 'return count(n)', 'return count(n)', 'dice_cached(5000)')]]),
'''To submit, use the program below, exactly the file programs/dice_table.py: the function followed by two lines that read n and print the answer.''',
judge('dice_table'),
python(['input'], 'reading n', '''`input()` reads one line of standard input as text and `int(…)` turns it into the number n. `print` writes the answer to standard output.'''),
f'''Judge notes. CSES reads standard input and compares standard output. Its time limit is 1 second, and its machines may be slower than a laptop: the loop above took {T_DICE:.1f} s locally, so if CPython is too slow choose the PyPy3 language option, which runs simple loops like this several times faster. Never submit dice_slow or dice_cached; they time out or stop with RecursionError. Print the remainder, not the exact count.''',
recap('ways[total] counts ordered sequences with that sum; ways[0] = 1 for the empty sequence.',
      'Group by the last face: add ways[total − face] for every face that fits.',
      'Take the remainder after every addition; it does not change the final remainder.',
      'Fill totals in increasing order: O(n) time, no recursion.')),
)

ch2 = chapter('Grid Paths: a count belongs to a cell', 'Transfer the last-move argument from a total to a row and a column.',
section('The Grid Paths problem', ['L2-09'], 'State the problem exactly before solving it.', 'Draw the legal routes in a small grid.',
grid_problem,
'''Rows and columns are numbered from 0 in our programs. The pair (r, c) identifies a cell: row r, column c. Neither coordinate is a count of routes.'''),
section('Draw the legal routes first', ['L2-09'], 'Find every route in a small grid by hand and state the movement rules precisely.', 'Count the routes into each cell from the cells above and to the left.',
'''Take the 3 by 3 grid with its centre blocked (rows ..., .*., ...). We cannot go backwards or diagonally, and a route that passes through the centre is not counted even if it later returns to open cells. Only the two routes around the outside remain.''',
diagram('L2-09'),
table(['Route', 'Moves', 'Cells visited'], [[str(i + 1), ', '.join(w), ' → '.join(K.grid_cells_of(w))] for i, w in enumerate(K.grid_routes(G3))], r'>{\raggedright\arraybackslash}p{12mm}XX')),
section('Count the two ways to enter a cell', ['L2-10'], 'Derive paths[r][c] = paths[r − 1][c] + paths[r][c − 1] for an open cell and fill the table.', 'Write the same rule as a recursive function.',
'''Let `paths[r][c]` count legal routes from the start to row r, column c. If the cell is open, the last move into it comes from immediately above or immediately to the left. Those groups are disjoint because their last moves differ, so we add the two counts. The picture shows every arrow into every open cell.''',
figure(F.grid_counts(G3, highlight=(2, 2)), 'The blocked-centre grid with the path count in each cell. Each open cell receives an arrow from above and from the left (thick arrows: the two that make 1 + 1 = 2 at the finish). The blocked cell stores 0 and passes nothing on.'),
'''Three different rules give an entry or a contribution, and they must be kept separate. A blocked cell has count 0. The open starting cell has count 1 for the empty route. A neighbour outside the top or left edge contributes 0. The table fills the cells row by row, left to right.''',
table(['Cell', 'Rule', 'From above', 'From the left', 'paths[r][c]'], K.grid_fill(G3), r'>{\raggedright\arraybackslash}p{12mm}>{\raggedright\arraybackslash}p{16mm}XX>{\raggedright\arraybackslash}p{18mm}'),
'''At (1, 1) the count is 0 because the cell itself is blocked, even though its neighbours have positive counts. At (1, 2) the count is 1 from above plus 0 from the left. At the destination (2, 2) it is 1 + 1 = 2.'''),
section('The recursive question has two coordinates', ['L2-11'], 'Write count(r, c) recursively, then cache it with @lru_cache.', 'Fill the table with loops instead, row by row.',
'''The recursive function asks for the number of routes to a cell. It first rejects coordinates outside the grid and blocked cells, then handles the open starting cell; every other cell asks the two predecessor questions. Each call moves one row up or one column left, so r + c decreases and the calls stop.''',
code('grid_slow', "print(grid_slow(['...', '.*.', '...']))"),
python(['or', 'strindex', 'nested'], 'or, and indexing a list of strings', '''`rows[r][c]` first picks the string for row r, then its character in column c. Python evaluates `or` from left to right and stops at the first true part, so `r < 0 or c < 0 or rows[r][c] == '*'` never reads `rows[-1]` for a negative r: the comparison `r < 0` is already true. Without that order, `rows[-1]` would silently read the last row.'''),
'''Several cells depend on the same earlier cell, so the slow version repeats work. Caching needs the pair (r, c) as its key, because a row number alone does not identify a cell.''',
code('grid_cached', "print(grid_cached(['...', '.*.', '...']))"),
python(['decorator'], '@lru_cache(None)', '''A line starting with @ above a function is a decorator: it wraps the function in extra behaviour. `@lru_cache(None)` from the `functools` module (imported on line 1) remembers the returned value for every combination of arguments; a later call with the same (r, c) returns the saved value without running the body. `None` means "no size limit". Because `count` is defined inside `grid_cached`, every new grid gets a fresh, empty cache.'''),
'''There are n² cells and at most two contributions per cell, so the cached version does O(n²) work. Its longest chain of calls is about 2n (the number of rows plus columns), so a 1,000 by 1,000 grid still exceeds Python's recursion limit.'''),
section('Make independent rows, then fill them in order', ['L2-12'], 'Fill paths row by row with loops, avoid the shared-row trap, and give the cost line by line.', 'Work the judge\'s 4 by 4 example.',
'''Visit rows from top to bottom and columns from left to right. When we reach cell (r, c), the cell above was computed in the previous row and the cell to the left earlier in the current row, so both answers are ready.''',
code('grid_table', "print(grid_table(['...', '.*.', '...']))"),
python(['listcomp', 'continue', 'ifexpr', 'negindex'], 'building a 2-D table; continue; x if c else y', '''`[[0] * n for _ in range(n)]` builds n separate rows; `_` is a loop variable whose value we do not need. By contrast `[[0] * n] * n` repeats one row object n times, so changing `paths[0][0]` changes every row. `continue` skips the rest of the loop body for this cell, leaving a blocked cell at 0. `paths[r - 1][c] if r > 0 else 0` is a conditional expression: the value before `if` when the test is true, otherwise the value after `else`. `paths[-1][-1]` is the last cell of the last row.'''),
cost('Cost of grid_table, line by line (blocked-centre 3 by 3 grid; full size: an open 1,000 by 1,000 grid)', 'grid_table', ((G3,), dict(n=3, b=1), 'Runs for the 3 by 3 grid'), (dict(n=1000, b=0), 'For n = 1,000'),
     [('for c in range(n):', 'n + 1 times per row', lambda n, b: n * (n + 1)),
      ("if rows[r][c] == '*':", 'once per cell', lambda n, b: n * n),
      ('if r == 0 and c == 0:', 'once per open cell', lambda n, b: n * n - b),
      ('paths[r][c] = (above + left) % MOD', 'once per open cell except the start', lambda n, b: n * n - b - 1)]),
f'''Constant work per cell: O(n²) time and O(n²) memory, a million cells at full size. On a laptop an open 1,000 by 1,000 grid took {T_GRID:.1f} s with CPython. The starting cell gets 1 only if it is open, because the blocked-cell test comes first.'''),
section('The judge\'s example, worked as a table', ['L2-13'], 'Check the method on the 4 by 4 example from the problem statement.', 'Collect the grid edge cases, mistakes and the judge submission.',
'''The judge's example has two blocked cells: (1, 2) and (2, 0). The same rule fills the table; the arrows show where each count comes from.''',
figure(F.grid_counts(G4, highlight=(3, 3), size=1.15), f'The 4 by 4 example with every count. The finish receives {K.grid_counts(G4)[2][3]} from above and {K.grid_counts(G4)[3][2]} from the left: {P.grid_table(G4)} paths.'),
table(['Row', 'Column 0', 'Column 1', 'Column 2', 'Column 3'], [[str(r)] + ['blocked' if G4[r][c] == '*' else str(K.grid_counts(G4)[r][c]) for c in range(4)] for r in range(4)]),
'''The seven paths, listed by their moves, confirm the count:''',
table(['Path', 'Moves (R = right, D = down)'], [[str(i + 1), ' '.join(m[0].upper() for m in w)] for i, w in enumerate(K.grid_routes(G4))], r'>{\raggedright\arraybackslash}p{12mm}X')),
section('Grid Paths: edge cases, mistakes and the judge', ['L2-13', 'L2-14'], 'Test the places where the rule changes and submit to CSES.', 'Compare the two problems of this lesson.',
edges([['1 by 1, open', '1', 'The start is the finish: one empty route.'],
       ['1 by 1, blocked', '0', 'The blocked check must come before the start rule.'],
       ['2 by 2, open', '2', 'Both predecessor directions: right-down and down-right.'],
       ['3 by 3, blocked centre', '2', 'Blocked cells interrupt routes without stopping the others.'],
       ['Blocked finish', '0', 'Many routes may reach its neighbours; none may enter it.'],
       ['1,000 by 1,000 open', C(P.grid_table(['.' * 1000] * 1000)), 'Needs the remainder and loops, not recursion.']]),
mistakes([['start rule before the blocked check', 'a blocked start gets 1', K.run_variant(GRID_START_FIRST, "grid_table(['*'])") + " on ['*'] (0)"],
          ['`[[0] * n] * n`', 'all rows are one shared list', K.variant('grid_table', 'paths = [[0] * n for _ in range(n)]', 'paths = [[0] * n] * n', "grid_table(['...', '.*.', '...'])") + ' (2)'],
          ['no bounds check in grid_slow', 'rows[−1] reads the last row, then runs off the grid', K.variant('grid_slow', 'if r < 0 or c < 0 or rows[r][c]', 'if rows[r][c]', "grid_slow(['..', '..'])")],
          ['grid_cached on 1,000 by 1,000', 'about 2,000 nested calls', 'RecursionError'],
          ['answer without % MOD', 'exact counts with hundreds of digits', 'wrong answer at the judge']]),
pause('Why must a blocked destination return 0 even if many routes reach its neighbours?', 'None of those routes may take the final step into a blocked cell. A positive predecessor count does not override the rule that the destination itself must be open.'),
'''To submit, use the program below, exactly the file programs/grid_table.py: the function followed by three lines that read the grid and print the answer.''',
judge('grid_table'),
python(['strip'], 'reading the rows', '''`input().strip()` reads one row and removes the invisible line ending (and any spaces) at its ends, so every row has exactly n characters. The list comprehension collects the n rows.'''),
'''Judge notes. CSES reads standard input; `input().strip()` removes the line ending from each row. A million cells is near the limit of what CPython does in 1 second on the judge, so choose PyPy3 if CPython times out. Never submit grid_slow or grid_cached.''',
recap('paths[r][c] counts routes to cell (r, c); a blocked cell is 0, the open start is 1.',
      'An open cell adds the counts from above and from the left; outside cells contribute 0.',
      'Fill rows top to bottom, columns left to right: O(n²).',
      'Build rows with a comprehension, never with [[0] * n] * n.')),
section('The shared counting idea', ['L2-14'], 'Name the common reason behind both recurrences and restate the main idea.', 'Use the summary tables to compare the programs.',
table(['', 'Dice', 'Grid Paths'], [['A stored answer', 'ways[total]: sequences with that sum', 'paths[r][c]: routes to that cell'],
                                  ['Ways to arrive', 'last face 1 to 6', 'from above or from the left'],
                                  ['Start', 'ways[0] = 1', 'paths[0][0] = 1 if open'],
                                  ['Impossible', 'faces that do not fit', 'blocked cells; outside the grid'],
                                  ['Order', 'increasing total', 'rows, then columns'],
                                  ['Answer', 'ways[n] % MOD', 'paths[n − 1][n − 1] % MOD']], r'>{\raggedright\arraybackslash}p{26mm}XX'),
'''That is the main idea of this lesson: count the ways to arrive. Every completed object belongs to exactly one last-move group. Removing that last move gives a smaller valid object, and appending it reverses the construction. We add group sizes because the groups cover all possibilities without overlapping; that is the reason for the recurrence in both problems.'''),
)

from dice_memory import book_chapter
ch3 = book_chapter()

appendix = [chapter('Summary tables', 'Reference tables for planning and for checking a student\'s claim quickly.',
section('Every algorithm in this lesson', [], 'Compare the cost of every program in one place.', 'Keep this page beside you while teaching.',
table(['Program', 'Time', 'Extra memory', 'Recursion depth', 'Use for'],
      [['dice_slow', 'exponential: 2ⁿ calls up to n = 6', 'O(n) stack', 'n + 1', 'tiny totals'],
       ['dice_cached', 'O(n)', 'O(n)', 'n + 1', 'showing the cache'],
       ['dice_table', 'O(n), about 6n steps', 'O(n)', 'none', 'the judge'],
       ['dice_123', 'O(n)', 'O(n)', 'none', 'the variation'],
       ['dice_ring', 'O(n)', 'O(1)', 'none', 'six counts'],
       ['dice_window', 'O(n)', 'O(1)', 'none', 'six counts and their sum'],
       ['grid_slow', 'exponential', 'O(n) stack', 'about 2n', 'tiny grids'],
       ['grid_cached', 'O(n²)', 'O(n²)', 'about 2n', 'showing the cache'],
       ['grid_table', 'O(n²)', 'O(n²)', 'none', 'the judge']], r'>{\raggedright\arraybackslash}p{22mm}X>{\raggedright\arraybackslash}p{18mm}>{\raggedright\arraybackslash}p{18mm}X'),
'''Here n is the target total or the side of the grid. The Python features explained in this book are sum over a generator, range with min, nested functions, dictionaries, the % operator, %=, tuples, list comprehensions, or, string indexing, decorators and @lru_cache, continue, conditional expressions and negative indices.'''),
section('Planning the two hours', [], 'See the lesson plan and what may move to the next meeting.', 'This is the end of the book; the teacher guide follows the same plan.',
table(['Minutes', 'Activity', 'Questions'], [[a, b, ('L2-' + c.replace('-', ' to L2-')) if c else ''] for a, b, c in __import__('content').LESSONS[1]['plan']], r'>{\raggedright\arraybackslash}p{16mm}X>{\raggedright\arraybackslash}p{26mm}'),
'''L2-04 and L2-05 mention the remainder before L2-06 explains it; in this book the remainder is explained first (section 1.5), and the same order works in class. The moving sum (L2-08) is optional and can be skipped. If the grid programs run long, L2-13 can be finished as homework with the local test files.'''))]

BOOK = dict(
    idea='To count the objects that end at a target, group them by how they arrive (their last move), make sure the groups do not overlap, and add the counts of the smaller targets they come from.',
    intro='Staircase counted routes by grouping them by their final jump. This lesson applies the same reasoning twice. Dice has up to six possible final values; a grid cell has at most two possible incoming moves. In each problem we first explain why the contributions are added, then make the computation fast: a cache, then a loop. Along the way we meet the remainder the judges ask for. After the Dice solutions, an optional chapter reduces memory by reusing six slots, then keeps their running sum.',
    outcomes=['state Dice Combinations and Grid Paths exactly and count small cases by hand;',
              'derive each recurrence by grouping objects by their last move;',
              'explain why taking remainders during the sums gives the right final remainder;',
              'write the recursive, cached and iterative programs and give their costs line by line;',
              'test the boundary cases and submit both programs to CSES.'],
    front=['Read this book before the lesson. The separate teacher guide holds the short classroom prompts and answers; the margin notes here name the matching question IDs on the worksheet, slides and notebook. Every program is printed in full, and every number about running code (call counts, line counts, wrong outputs, timings) was produced by running the programs.',
           'Students need Lesson 1 (a recurrence, a cache, a table filled in order) and Python functions, lists and loops. Each new Python feature is explained in a grey PYTHON note beside the first program that uses it.',
           'Each section opens with its objective and ends by pointing to the next. Each problem ends with its edge cases, common mistakes (with the wrong output each one produces), how to submit it and a recap. The summary tables and the two-hour plan are in the appendix.'],
    chapters=[ch1, ch3, ch2], appendix=appendix)
