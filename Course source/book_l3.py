"""Lesson 3 tutor book: Mortal Kombat Tower and Array Description. Main idea: remember the missing detail."""
import programs as P
import book_kit as K
import book_figures as F
from book_blocks import (section, chapter, code, diagram, table, pause, figure, python,
                         problem, items, recap, listing, judge, cost, edges, mistakes)

C = K.comma
B4 = [1, 0, 1, 1]
BJ = [1, 1, 0, 1, 1, 1]
A4, M = [2, 0, 0, 1], 3
TOWER_ROWS, FRIEND, YOU = K.tower_fill(B4)
ARRAY_ROWS, ARRAY_TABLE = K.array_fill(A4, M)
STATES, _ = K.array_completions(A4, M)
OVER, GOOD, BAD = F.overwrite_picture()
T_TOWER = K.seconds(P.tower_table, ([i % 2 for i in range(200000)],))
T_ARRAY = K.seconds(P.array_rolling, ([0] * 100000, 100))
sched = lambda b: '; '.join(f'{p} takes ' + ' and '.join(map(str, i)) for p, i in K.tower_schedule(b))

tower_problem = problem(
    name='Mortal Kombat Tower',
    story='You and a friend beat the bosses of a tower together, but your friend needs help with the hard ones.',
    rules='A tower has n bosses, numbered 0 to n − 1, which must be beaten in order. Each boss is easy (0) or hard (1). You and your friend take turns, and your friend has the first turn. On a turn the player beats the next boss or the next two bosses: never none, never three. You can beat any boss for free. Your friend can beat an easy boss for free, but pays one point (the judge calls it a skip point) for every hard boss he beats. Both of you cooperate to make the friend\'s total as small as possible. Find that total.',
    input='the first line holds t, the number of towers. For each tower one line holds n and the next holds the n boss types.',
    output='one line per tower: the smallest number of points.',
    limits='1 ≤ t ≤ 20,000; 1 ≤ n ≤ 200,000; all towers together have at most 200,000 bosses. The time limit is on the problem page.',
    example_in='1\n6\n' + ' '.join(map(str, BJ)), example_out=str(P.tower_table(BJ)),
    why='One tower. ' + sched(BJ) + '. The friend pays for bosses 0 and 3.',
    source='Codeforces, problem 1418C.', url='https://codeforces.com/problemset/problem/1418/C')

array_problem = problem(
    name='Array Description',
    story='Some numbers in a list have been rubbed out. In how many ways can they be filled back in?',
    rules='A list has n whole numbers, each from 1 to m, and any two neighbours differ by at most 1. Some entries are known; the missing ones are written 0. Count the ways to fill every missing entry so that the rules hold. A 0 is a placeholder, never a value of the completed list.',
    input='the first line holds n and m; the second holds the n entries.',
    output='the number of ways, as its remainder after dividing by 1,000,000,007.',
    limits='1 ≤ n ≤ 100,000; 1 ≤ m ≤ 100; every entry is from 0 to m. The judge allows 1 second and 512 MB.',
    example_in='4 3\n2 0 0 1', example_out=str(P.array_rolling(A4, M)),
    why='The five completed lists are ' + ', '.join(str(a) for a in K.array_fillings(A4, M)) + '.',
    source='CSES Problem Set, task 1746.', url='https://cses.fi/problemset/task/1746')

ch1 = chapter('The tower: whose turn comes next?', 'Define a state that determines both the available choices and their cost.',
section('The Mortal Kombat Tower problem', ['L3-01', 'L3-02'], 'State the problem exactly before solving it.', 'See why the boss position alone is not enough.',
'''This lesson has one main idea: remember the missing detail. In Lessons 1 and 2 a single number (a step, a stone, a total, a cell) identified each question. Here two situations at the same position can have different answers, and we must find the extra detail that tells them apart.''',
tower_problem,
'''In this book the two players are always called "your friend" and "you", and the code uses the lists `friend` and `you`. "Points" are what your friend pays.'''),
section('Why a position alone is not enough', ['L3-01', 'L3-02'], 'Find, with a one-boss example, the detail that the position forgets.', 'Define the remaining-cost question with both details.',
'''Suppose one hard boss remains. If it is your turn you beat it for free; if it is your friend's turn it costs one point. The next boss index is the same, but the remaining cost differs. We therefore need both the position and the player who moves next.

A state is the information that identifies a subproblem. Two situations may share an answer only if that information determines the same remaining choices and costs. The player field is needed for that reason, not to make a two-dimensional table.''',
'''Now the classroom example: bosses [1, 0, 1, 1]. The strip shows one cheapest schedule: shaded bosses are beaten by your friend, white ones by you.''',
figure(F.boss_strip(B4), 'Bosses [1, 0, 1, 1]: your friend takes bosses 0 and 1 and pays 1; you take bosses 2 and 3 for free. Total: 1.'),
'''This schedule is optimal. The friend must beat the first boss, because the friend starts and cannot take zero bosses; that boss is hard, so at least one point is unavoidable. The schedule attains one point, so no cheaper schedule exists. The judge's example works the same way:''',
figure(F.boss_strip(BJ), f'The judge\'s example [1, 1, 0, 1, 1, 1]: {sched(BJ)}. Total {P.tower_table(BJ)}.')),
section('Ask for the cheapest remaining cost', ['L3-03', 'L3-04'], 'Define cost(i, friend_turn), its stopping case and recurrence, and write the cached program.', 'Turn the recurrence into two lists filled backwards.',
'''Let cost(i, friend_turn) be the fewest additional points needed to finish the bosses from index i onwards. `friend_turn` is True when your friend moves next and False when you move next. The value is a future cost: it does not include points paid before position i.

If i equals the number of bosses, none are left and the remaining cost is 0 for either player. Otherwise try taking one boss and, if two remain, two. Add the cost of that turn to the cheapest continuation with the other player next. For the friend the turn costs the number of hard bosses taken; for you it costs 0. Both players want the friend's total small, so we take the minimum on both players' turns.''',
table(['State', 'Take 1 boss', 'Take 2 bosses (if i + 1 < n)'], [['cost(i, True)', 'bosses[i] + cost(i + 1, False)', 'bosses[i] + bosses[i + 1] + cost(i + 2, False)'], ['cost(i, False)', '0 + cost(i + 1, True)', '0 + cost(i + 2, True)'], ['cost(n, either)', '0', '']], r'>{\raggedright\arraybackslash}p{26mm}XX'),
code('tower_cached', 'print(tower_cached([1, 0, 1, 1]))'),
python(['decorator', 'nested', 'inf', 'slice', 'not', 'sum', 'ifexpr', 'min'], "@lru_cache, float('inf'), slices, x if c else y, not", '''`@lru_cache(None)` (from `functools`, line 1) makes `cost` remember its answer for every pair (i, friend_turn); `cost` is nested inside `tower_cached`, so each tower gets a fresh cache. `float('inf')` is infinity, a starting value larger than any real cost, so the first `min` always replaces it. `bosses[i:i + take]` is a slice: the entries from index i up to, but not including, i + take; `sum` adds them. `sum(bosses[i:i + take]) if friend_turn else 0` is a conditional expression: the sum when it is the friend's turn, otherwise 0. `min(answer, x)` keeps the smaller value. `not friend_turn` swaps True and False: the other player moves next.'''),
'''The cache key contains both i and the Boolean; a key of just i would merge situations with different next players. Each call moves to a larger index, so the recursion stops. There are at most 2(n + 1) states and two choices per state, so caching makes the work O(n), although the chain of calls can still be n long.'''),
section('Two lists filled from the end', ['L3-05'], 'Fill friend[i] and you[i] from i = n down to 0, with every comparison written out.', 'Check the ends of the tower and collect the mistakes.',
'''Let `friend[i]` be the least remaining cost when your friend moves next at boss i, and `you[i]` the same when you move next. The stopping entries `friend[n]` and `you[n]` are 0, because position n lies just after the last boss. Each entry reads positions i + 1 and perhaps i + 2:''',
figure(F.tower_dependencies(B4, 1), 'The two lists for [1, 0, 1, 1], with the entries read when position 1 is filled.'),
'''Because every entry reads later positions, we fill from the end towards the beginning. This is the opposite direction from Frog's table, where an entry was the cost from the start; the meaning of the stored answer decides the direction. Position 4 is preset to 0 and the loop fills positions 3 down to 0:''',
table(['i', 'Boss', 'Friend moves next', 'friend[i]', 'You move next', 'you[i]'], TOWER_ROWS, r'>{\raggedright\arraybackslash}p{5mm}>{\raggedright\arraybackslash}p{9mm}X>{\raggedright\arraybackslash}p{14mm}X>{\raggedright\arraybackslash}p{12mm}'),
code('tower_table', 'print(tower_table([1, 0, 1, 1]))'),
python(['range', 'negstep', 'listmul', 'min'], 'range(n − 1, −1, −1) and the two lists', '''`[0] * (n + 1)` makes a list of n + 1 zeros, positions 0 to n, so `friend[n]` and `you[n]` start at 0 as required; `min` keeps the cheaper choice. `range(start, stop, step)` with step −1 counts down: `range(n - 1, -1, -1)` gives n − 1, n − 2, …, 1, 0. The stop value −1 is excluded, exactly as the stop value is excluded when counting up, so 0 is the last index visited.'''),
cost('Cost of tower_table, line by line', 'tower_table', ((B4,), dict(n=4), 'Runs for [1, 0, 1, 1]'), (dict(n=200000), 'For n = 200,000'),
     [('for i in range(n - 1, -1, -1):', 'n times, plus the final check', lambda n: n + 1),
      ('friend[i] = bosses[i] + you[i + 1]', 'once per position', lambda n: n),
      ('pay = bosses[i] + bosses[i + 1]', 'once per position except the last', lambda n: n - 1)]),
f'''The answer is `friend[0]`: no bosses are beaten yet and your friend starts. The entry `you[0]` describes a different start, so it is not the answer. Time and memory are O(n); a 200,000-boss tower took {T_TOWER*1000:.0f} ms locally.'''),
section('Tower: edge cases, mistakes and the judge', ['L3-06'], 'Test the ends of the tower and submit to Codeforces.', 'Move to Array Description, where the missing detail is a value.',
edges([['[0]', str(P.tower_table([0])), 'One easy boss: the friend must take it, for free.'],
       ['[1]', str(P.tower_table([1])), 'One hard boss: the friend must take it; taking two is out of range.'],
       ['[1, 1, 1]', str(P.tower_table([1, 1, 1])), 'Friend takes one, you take two: taking as many as possible first is not always best.'],
       ['200,000 hard bosses', C(P.tower_table([1] * 200000)), 'The friend pays every third boss; needs the loop.']]),
mistakes([['`return min(friend[0], you[0])`', 'lets you take the first turn', K.variant('tower_table', 'return friend[0]', 'return min(friend[0], you[0])', 'tower_table([1])') + ' on [1] (1)'],
          ['no `i + 1 < n` check', 'reads bosses[n] at the last boss', K.variant('tower_table', 'if i + 1 < n:', 'if True:', 'tower_table([1])') + ' on [1]'],
          ['loop from 0 upwards', 'reads entries that are still 0', K.variant('tower_table', 'range(n - 1, -1, -1)', 'range(n)', f'tower_table({BJ})') + f' on the judge example ({P.tower_table(BJ)})'],
          ['friend pays on your turns too', 'charges every hard boss', K.variant('tower_cached', ' if friend_turn else 0', '', 'tower_cached([1, 0, 1, 1])') + ' (1)'],
          ['tower_cached on 200,000 bosses', 'a chain of 200,000 calls', 'RecursionError']]),
'''To submit, use the program below, exactly the file programs/tower_table.py. It reads t, then for each tower its length and its bosses, and prints one answer per tower.''',
judge('tower_table'),
python(['input', 'map', 'split'], 'reading many towers', '''`int(input())` reads one line as a number. `for _ in range(tests):` repeats the reading and solving once per tower; `_` is a loop variable we do not need. `list(map(int, input().split()))` cuts a line into words and converts each to an integer.'''),
'''Judge notes. Codeforces reads standard input. The input may hold 20,000 towers, so the program calls `tower_table` once per tower; the total work is still O(total bosses). Python 3 and PyPy 3 are both offered; PyPy is the safer choice for input this large. Do not submit the recursive version.''',
recap('The state is (position, who moves next); the position alone forgets whose turn it is.',
      'friend[i] = bosses taken + you[later]; you[i] = friend[later]; take the minimum over 1 or 2 bosses.',
      'Entries read later positions, so fill from n − 1 down to 0; the answer is friend[0].',
      'O(n) time and memory.')),
)

ch2 = chapter('Array Description: the previous value matters', 'Count valid fillings while keeping the value needed to check the next neighbour.',
section('The Array Description problem', ['L3-07'], 'State the problem exactly before solving it.', 'List the fillings of the example and find the missing detail.',
array_problem,
'''We use n for the number of entries and m for the largest allowed value, in the text and in the code. Position i is an index from 0; v is a value placed at a position.'''),
section('A zero marks an unknown entry', ['L3-07'], 'Enumerate the completed arrays and see why the position alone cannot be the state.', 'Count completions recursively, remembering the previous value.',
'''For [2, 0, 0, 1] with m = 3, every completed array is listed below. A missing zero must be replaced; zero is not an allowed value of the completed array.''',
table(['Completed array', 'Position 1', 'Position 2'], [[str(a), str(a[1]), str(a[2])] for a in K.array_fillings(A4, M)], r'>{\raggedright\arraybackslash}p{40mm}XX'),
'''Suppose we have filled the same number of positions in two ways, one ending in 1 and the other in 3. With values 1 to 3, the first may continue with 1 or 2; the second with 2 or 3. Position alone does not determine the next legal choices: the last value must also be remembered. That is the missing detail.'''),
section('Count completions recursively', ['L3-09'], 'Define count(i, previous), write the cached program and see its cost.', 'Change the meaning to prefixes and fill a table.',
'''For recursion, let count(i, previous) be the number of ways to fill positions i onwards, given the value immediately before position i. Here i is the next position to fill and previous is a value, not a position. Try each candidate value; reject it if the input fixes position i to a different value, or (except at position 0) if it differs from previous by more than 1. For each surviving candidate move to i + 1 with that candidate as the new previous value, and add the returned counts. When i reaches n every position is filled legally: return 1.''',
code('array_cached', 'print(array_cached([2, 0, 0, 1], 3))'),
python(['decorator', 'continue', 'abs', 'neq', 'mod'], 'continue, != , % and the sentinel', '''`answer % MOD` keeps the remainder after dividing by MOD = 1,000,000,007 (line 3), as in Lesson 2. `!=` means "is not equal to". `continue` skips the rest of the loop body and moves to the next candidate value. The first call passes previous = 0 as a sentinel: a marker meaning "no previous entry". The test `i == 0 or …` skips the neighbour check at position 0, so the sentinel is never compared with a real value. `@lru_cache(None)` remembers every (i, previous) state.'''),
'''The table lists every state the example visits, from the last position back to the first. Each value is the number of ways to complete the array from that state.''',
table(['State count(i, previous)', 'Completions'], [[f'count({i}, {p})' + (' (start: no previous)' if i == 0 else ''), str(v)] for (i, p), v in sorted(STATES.items(), reverse=True)], r'>{\raggedright\arraybackslash}p{60mm}X'),
cost('Cost of array_cached on an array of n zeros, line by line', 'array_cached', (([0] * 4, 3), dict(n=4, m=3), 'Runs for n = 4, m = 3'), (dict(n=100000, m=100), 'For n = 100,000, m = 100'),
     [('answer = 0', 'once per state: 1 + (n − 1) × m', lambda n, m: 1 + (n - 1) * m),
      ('if values[i] != 0 and values[i] != value:', 'm times per state', lambda n, m: m * (1 + (n - 1) * m))]),
'''So this teaching version is O(n × m²): there are about n × m states and each tries all m values, which at full size is about a billion steps. It is also n calls deep. The table that follows reads only three predecessor values per cell.'''),
section('Count prefixes with a table', ['L3-08', 'L3-10'], 'Define table[i][v] for prefixes and fill it with every sum written out.', 'Keep only two rows.',
'''For iteration we use a different but explicit meaning. Let `table[i][v]` count valid fillings of positions 0 to i whose value at position i is v. This counts already-filled prefixes, whereas the recursive function counted future completions; both solve the problem, but their intermediate numbers answer different questions.

A new value v can follow v − 1, v or v + 1, the only values within distance 1. The three groups are disjoint because their previous values differ, so their counts are added. If the input fixes position i to another value, the count for v is 0. Two extra columns, 0 and m + 1, always hold 0: they are padding, not possible values, and make the three-term sum work at the edges.''',
figure(F.array_dependencies(A4, M, 3, 1), 'The table for [2, 0, 0, 1], m = 3. Grey columns are padding. The arrows show the three entries of row 2 that table[3][1] adds: 0 + 2 + 3 = 5.'),
table(['Position i', 'Given', 'v = 1', 'v = 2', 'v = 3'], ARRAY_ROWS, r'>{\raggedright\arraybackslash}p{16mm}>{\raggedright\arraybackslash}p{10mm}XXX'),
f'''The final position is fixed to 1, so only its first column is non-zero: 2 + 3 = 5 (plus 0 from the padding). In general we sum every column of the last row, because the last value need not be fixed.''',
code('array_full', 'print(array_full([2, 0, 0, 1], 3))'),
python(['listcomp', 'membership', 'sum', 'listmul', 'mod', 'negindex'], 'tables, "in", sum and table[-1]', '''`[[0] * (m + 2) for _ in values]` builds one separate row of m + 2 zeros per entry of `values`. `values[0] in (0, value)` is True when the entry is missing (0) or equals the candidate. `table[-1]` is the last row, and `sum(table[-1])` adds it; the padding columns contribute 0. Every count is kept as a remainder with `% MOD`.'''),
'''Each of the n rows has m values and each reads three counts: O(n × m) time and memory.'''),
section('Keep the old row intact while building the new row', ['L3-11'], 'Use two rows, before and now, and see exactly what goes wrong when one row is updated in place.', 'Try a fresh example, then collect the mistakes and the judge submission.',
'''Every new row reads only the previous one, so we keep `before` (counts ending at the previous position) and `now` (counts ending at the current position). Once `now` is complete we assign `before = now`. While building now, every contribution must come from before. If we overwrote before one column at a time, later columns would read counts that already belong to the current position:''',
figure(OVER, 'Two rows versus one row updated in place, starting from counts [1, 1, 1].'),
code('array_rolling', 'print(array_rolling([2, 0, 0, 1], 3))'),
python(['rebind'], 'before = now', '''`before = now` makes the name `before` refer to the list just built; no numbers are copied. The next round creates a brand-new list for `now` (line 9), so the two names never refer to the same list while a row is being filled.'''),
cost('Cost of array_rolling, line by line', 'array_rolling', ((A4, M), dict(n=4, m=3), 'Runs for the example'), (dict(n=100000, m=100), 'For n = 100,000, m = 100'),
     [('for i in range(1, len(values)):', 'n times, including the final check', lambda n, m: n),
      ('if values[i] in (0, value):', 'm times per position after the first', lambda n, m: (n - 1) * m),
      ('before = now', 'once per position after the first', lambda n, m: n - 1)]),
f'''Time stays O(n × m), about ten million cell updates at full size, but storage falls to O(m) because only two rows are kept (the input list itself still takes O(n)). Locally the full-size case took {T_ARRAY:.1f} s with CPython.'''),
section('Use a fresh example to check the meaning', ['L3-12'], 'Check the table on [0, 0, 3] and an impossible fixed pair.', 'Collect the edge cases, mistakes and the judge submission.',
table(['Position i', 'Given', 'v = 1', 'v = 2', 'v = 3'], K.array_fill([0, 0, 3], 3)[0], r'>{\raggedright\arraybackslash}p{16mm}>{\raggedright\arraybackslash}p{10mm}XXX'),
'''The five arrays are ''' + ', '.join(str(a) for a in K.array_fillings([0, 0, 3], 3)) + '''. A fixed array [1, 3] has no valid filling: the neighbours already differ by 2 and no missing position can repair them; the recurrence gives 0 naturally.'''),
section('Array Description: edge cases, mistakes and the judge', [], 'Prepare students to test the program and submit it to CSES.', 'Compare the two problems of the lesson.',
edges([['[0], m = 3', str(P.array_rolling([0], 3)), 'One missing entry, no neighbour: any value.'],
       ['[1, 3], m = 3', str(P.array_rolling([1, 3], 3)), 'Fixed neighbours too far apart: no special case needed.'],
       ['[0, 0, 0], m = 1', str(P.array_rolling([0, 0, 0], 1)), 'Only value 1; both padding columns are used at once.'],
       ['[5, 0], m = 5', str(P.array_rolling([5, 0], 5)), 'Value m at the right edge reads the right padding column.'],
       ['100,000 zeros, m = 100', C(P.array_rolling([0] * 100000, 100)), 'Full size: needs the remainder and two rows.']]),
mistakes([['ignore fixed entries after the first', 'counts arrays that change given values', K.variant('array_rolling', '            if values[i] in (0, value):', '            if True:', 'array_rolling([2, 0, 0, 1], 3)') + ' (5)'],
          ['first row all ones', 'ignores a fixed first entry', K.variant('array_rolling', 'if values[0] in (0, value):', 'if True:', 'array_rolling([2, 0, 0, 1], 3)') + ' (5)'],
          ['one row updated in place', 'reads counts of the current position', K.variant('array_rolling', 'now = [0] * (m + 2)', 'now = before', 'array_rolling([2, 0, 0, 1], 3)') + ' (5)'],
          ['no padding: rows of m + 1', 'reads index m + 1 at v = m', K.variant('array_rolling', '[0] * (m + 2)', '[0] * (m + 1)', 'array_rolling([2, 0, 0, 1], 3)', 2)],
          ['array_cached on 5,000 zeros', 'the chain of calls is 5,000 deep', K.variant('array_cached', 'return count(0, 0)', 'return count(0, 0)', 'array_cached([0] * 5000, 3)')]]),
'''To submit, use the program below, exactly the file programs/array_rolling.py.''',
judge('array_rolling'),
python(['map', 'split'], 'n, m = …', '''`n, m = map(int, input().split())` reads the first line, converts both words to integers and assigns them to two names at once. The second line becomes the list `values` in the same way.'''),
f'''Judge notes. CSES reads standard input; the first line gives n and m, the second the entries. The time limit is 1 second and the full-size case took {T_ARRAY:.1f} s locally with CPython, so choose PyPy3. Print the remainder.''',
recap('The state is (position, last value); the position alone forgets which values may come next.',
      'table[i][v] = table[i − 1][v − 1] + table[i − 1][v] + table[i − 1][v + 1], or 0 if position i is fixed to another value.',
      'Padding columns 0 and m + 1 hold 0; the answer sums the last row.',
      'Build each new row from an untouched old row: O(n × m) time, O(m) memory.')),
section('What information changes the future?', ['L3-13'], 'Compare the two missing details and restate the main idea.', 'Use the practice files to test both programs.',
table(['', 'Tower', 'Array Description'], [['Position alone forgets', 'whose turn it is', 'the previous value'],
                                          ['State', '(i, who moves next)', '(i, value at i)'],
                                          ['Stored value', 'least remaining cost', 'number of valid prefixes'],
                                          ['Combine with', 'min', '+'],
                                          ['Order', 'i from n − 1 down to 0', 'i from 1 up to n − 1'],
                                          ['Answer', 'friend[0]', 'sum of the last row']], r'>{\raggedright\arraybackslash}p{30mm}XX'),
'''The tower keeps the next player because that player changes future costs. Array Description keeps the previous value because it changes future legal choices. In both, earlier history can be forgotten once the kept information is enough to answer the remaining question. That is the main idea of the lesson: remember the missing detail. To invent a state, start with the position, look for two histories at the same position with different futures, and add exactly the detail that separates them.''',
pause('Why can we not merge the three counts in a row into one total before processing the next position?', 'The next value may follow only some previous values. Once their counts are merged, we no longer know which part of the total comes from a legal predecessor.')),
)

appendix = [chapter('Summary tables', 'Reference tables for planning and for checking a student\'s claim quickly.',
section('Every algorithm in this lesson', [], 'Compare the cost of every program in one place.', 'Keep this page beside you while teaching.',
table(['Program', 'Time', 'Extra memory', 'Recursion depth', 'Use for'],
      [['tower_cached', 'O(n)', 'O(n)', 'n', 'showing the state'],
       ['tower_table', 'O(n)', 'O(n)', 'none', 'the judge'],
       ['array_cached', 'O(n × m²)', 'O(n × m)', 'n', 'small examples'],
       ['array_full', 'O(n × m)', 'O(n × m)', 'none', 'drawing the table'],
       ['array_rolling', 'O(n × m)', 'O(m)', 'none', 'the judge']], r'>{\raggedright\arraybackslash}p{24mm}X>{\raggedright\arraybackslash}p{18mm}>{\raggedright\arraybackslash}p{18mm}X'),
'''The Python features explained in this book are @lru_cache, nested functions, float('inf'), slices, not, sum, range with step −1, continue, !=, abs, list comprehensions, the in test and reassigning a name to a list.'''),
section('Planning the two hours', [], 'See the lesson plan and what may move to the next meeting.', 'This is the end of the book; the teacher guide follows the same plan.',
table(['Minutes', 'Activity', 'Questions'], [[a, b, ('L3-' + c.replace('-', ' to L3-')) if c else ''] for a, b, c in __import__('content').LESSONS[2]['plan']], r'>{\raggedright\arraybackslash}p{16mm}X>{\raggedright\arraybackslash}p{26mm}'),
'''L3-08 (what a prefix count means) is taught here together with the table (section 2.4), next to L3-10, so the meaning changes only once: the recursion counts completions, the table counts prefixes. If the lesson runs long, keep the rolling-row program (L3-11) as follow-up; understanding the full table is the core goal.'''))]

BOOK = dict(
    idea='When the position alone does not decide what can happen next, find the one extra detail that does (whose turn it is, or the previous value) and make it part of the state; forget everything else.',
    intro='In the first two lessons a step, stone, total or cell identified each question. Now we meet problems where the position alone loses essential information. In the tower, whose turn it is changes the price of the same boss. In Array Description, the previous value changes which values may come next. We find that missing detail with small examples before adding it to a function or a table.',
    outcomes=['state both problems exactly and solve small cases by hand;',
              'find the missing detail with two histories that share a position but not a future;',
              'fill a table backwards (tower) and forwards (arrays), with every entry worked;',
              'explain why the new row must be built from an untouched old row;',
              'give the cost of each program line by line and submit both to their judges.'],
    front=['Read this book before the lesson. The separate teacher guide holds the short classroom prompts and answers; the margin notes here name the matching question IDs on the worksheet, slides and notebook. Every program is printed in full, and every number about running code (line counts, wrong outputs, timings) was produced by running the programs.',
           'Students need Lessons 1 and 2 (recurrences, caches, tables filled in order, remainders) and Python functions, lists and loops. Each new Python feature is explained in a grey PYTHON note beside the first program that uses it.',
           'Each section opens with its objective and ends by pointing to the next. Each problem ends with its edge cases, common mistakes (with the wrong output each one produces), how to submit it and a recap. The summary tables and the two-hour plan are in the appendix.'],
    chapters=[ch1, ch2], appendix=appendix)
