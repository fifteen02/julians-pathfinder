"""Lesson 5 tutor book: Hoof, Paper, Scissors. Main idea: choose when to switch."""
from itertools import product
import programs as P
import book_kit as K
import book_figures as F
from book_blocks import (section, chapter, code, diagram, table, pause, figure, python,
                         problem, items, recap, listing, judge, cost, edges, mistakes)

C = K.comma
J = 'HHSSP'
LAYERS, WORK = K.hps_layers(J, 1)
TRANS, TRANS_VALUE = F.hps_transition(J, 2, 1, 'H')
FULLJ = ''.join('HPS'[i % 3] * (4762 if i < 20 else 4760) for i in range(21))
T_HPS = K.seconds(P.hps_table, (FULLJ, 20))
best_s = lambda j, k: K.hps_best_strategy(j, k)
work_cols = r'>{\raggedright\arraybackslash}p{11mm}>{\raggedright\arraybackslash}p{9mm}>{\raggedright\arraybackslash}p{9mm}>{\raggedright\arraybackslash}p{12mm}>{\raggedright\arraybackslash}p{9mm}X>{\raggedright\arraybackslash}p{8mm}>{\raggedright\arraybackslash}p{23mm}'
work_head = ['Round', 'John', 'used', 'Bessie', 'Stay', 'Switch from (used − 1)', 'Win', 'now[used][g]']
# The -inf start value cannot be replaced by 0 without being misleading; check whether
# it changes any answer on all games up to 5 rounds and budgets up to 2.
ZERO_SAME = all(K.variant('hps_table', "impossible = -float('inf')", 'impossible = 0', f'hps_table({"".join(s)!r}, {k})') == repr(P.hps_table(''.join(s), k))
                for n in range(1, 6) for s in product('HPS', repeat=n) for k in range(3))

hps_problem = problem(
    name='Hoof, Paper, Scissors',
    story='Bessie knows every move Farmer John will make, but she is too lazy to change her own move often.',
    rules='Bessie and Farmer John play N rounds of hoof, paper, scissors, written H, P and S. Hoof beats scissors, scissors beats paper and paper beats hoof; the same gesture twice is a draw. Bessie knows all of John\'s gestures in advance. She picks any gesture for the first round; after that she may change her gesture at most K times in all (the first choice is free). What is the largest number of rounds she can win? (In our code N is len(john) and K is budget.)',
    input='the file hps.in holds N and K on its first line, then John\'s N gestures, one per line.',
    output='write the largest number of wins to the file hps.out.',
    limits='1 ≤ N ≤ 100,000; 0 ≤ K ≤ 20. The problem page states no time limit.',
    example_in='5 1\nH\nH\nS\nS\nP', example_out=str(P.hps_table(J, 1)),
    why='Bessie plays P, P, then changes once to H and keeps it: she wins rounds 0 to 3 and loses the last. The judge\'s own sample is six rounds, HHSSPP with K = 1 (answer ' + str(P.hps_table('HHSSPP', 1)) + '); this book uses the five rounds HHSSP throughout, as the worksheet and slides do.',
    source='USACO 2017 January contest, Gold, problem 2.', url='http://www.usaco.org/index.php?page=viewproblem2&cpid=694')

ch1 = chapter('Understand what a switch buys us', 'Find concrete strategies before defining a multidimensional state.',
section('The Hoof, Paper, Scissors problem', ['L5-01'], 'State the problem exactly before solving it.', 'Score the strategies that never switch.',
'''This lesson has one main idea: choose when to switch. Bessie's only real decisions are the moments at which she changes gesture, and each change spends from a small budget. The state will record exactly what the future needs to know about those decisions.''',
hps_problem,
'''Names used throughout: rounds are numbered from 0; `john` is John's sequence; `budget` is the judge's K; `used` is the number of switches already spent; g (or gesture) is Bessie's current gesture.'''),
section('Score one fixed gesture', ['L5-01', 'L5-02'], 'Compute the best score with no switches.', 'Place one switch by hand.',
'''A win scores 1; a draw or loss scores 0. If Bessie keeps one gesture for all of HHSSP:''',
table(['Bessie always plays', 'Wins round by round', 'Total'], K.hps_fixed(J), r'>{\raggedright\arraybackslash}p{30mm}X>{\raggedright\arraybackslash}p{14mm}'),
f'''With no switches allowed the best score is therefore {P.hps_table(J, 0)}. Choosing the first gesture costs no switch because there is no earlier gesture, so all three fixed strategies are available with a budget of 0. A switch happens only when Bessie's gesture changes between consecutive rounds.'''),
section('One well-placed switch', ['L5-03'], 'Find the best one-switch strategy and prove that five wins are impossible.', 'Find the information the future needs.',
'''Allow one switch. A one-switch strategy plays one gesture for a first block of rounds and another for the rest. The table tries every place for the switch, choosing the best gesture for each block.''',
table(['Switch before round', 'First block', 'Second block', 'Best strategy', 'Wins'],
      [[str(k), J[:k], J[k:], s, str(w)] for k in range(1, len(J))
       for s, _, w in [max(((a * k + b * (len(J) - k), 1, sum(P.BEATS[x] == y for x, y in zip(a * k + b * (len(J) - k), J))) for a in 'HPS' for b in 'HPS' if a != b), key=lambda t: t[2])]]),
f'''The best is {best_s(J, 1)[0]} with {best_s(J, 1)[2]} wins: the two Ps beat John's first two Hs; after changing to H, Bessie wins the next two rounds against S; the last H loses to P. To win all five rounds Bessie would need P, P, H, H, S, which needs two switches. So with a budget of one, four wins is optimal.''',
diagram('L5-03'),
'''The problem allows at most the given number of switches, so a strategy may leave some unused: if John always plays H, Bessie wins every round by keeping P, however many switches are allowed.'''),
section('Identify the information the future needs', ['L5-04'], 'Show that round and switches used are not enough, and choose the state.', 'Write the recursive version.',
'''Suppose two partial strategies have played the same rounds and used the same number of switches, but one currently plays H and the other P. Choosing H next costs nothing for the first but one switch for the second. Their futures differ, so we cannot merge them into one score.

A useful state therefore records the rounds processed, the number of switches used and the current gesture. Its stored value is the greatest number of wins among strategies with exactly those three properties. When two histories agree in all three fields, the one with fewer wins can be discarded: every continuation open to it is open to the other and earns the same future wins.'''),
)

ch2 = chapter('Build the recurrence and trace the scores', 'Separate switches used, the remaining budget and the score stored in a cell.',
section('A recursive view: choose the next gesture', ['L5-05'], 'Define best(i, left, previous) and write the cached program.', 'Switch to the table view and its first round.',
'''For recursion, let best(i, left, previous) be the largest number of wins from round i onwards, with left switches still available and previous as Bessie's previous gesture. The returned score does not include wins before round i. Try H, P and S. A candidate costs a switch exactly when a previous gesture exists and the candidate differs from it; reject it if that needs more switches than left. Otherwise add this round's win to the best continuation. At the start, previous is the empty string, so the first choice is free. After the last round no wins remain: return 0.''',
code('hps_cached', "print(hps_cached('HHSSP', 1))"),
python(['decorator', 'nested', 'dict', 'int-bool', 'strloop', 'max'], 'BEATS, int(True) and looping over a string', '''`BEATS = {'H': 'S', 'P': 'H', 'S': 'P'}` is a dictionary from Bessie's gesture to the gesture it beats, so `BEATS['H'] == 'S'`. A comparison gives True or False, and `int(True)` is 1 and `int(False)` is 0: line 11 turns "this choice is a switch" into a cost of 1 or 0, and line 13 turns "this gesture wins" into 1 or 0. `for gesture in 'HPS':` loops over the characters of a string. `@lru_cache(None)` remembers each (i, left, previous) answer.'''),
f'''This version is a clear reference for small inputs: it visits {K.calls(P.hps_cached, (J, 1), 'best')} states on HHSSP. There are about N × (K + 1) × 4 states and three candidates each, but the chain of calls is N long, so it stops with RecursionError on long games. The table version avoids the stack. Note the change of viewpoint: the recursion counts switches left and returns future wins; the table counts switches used and stores wins already earned.'''),
section('Initialise after the first round', ['L5-06'], 'Define before[used][g] and fill it after round 0, with impossible states marked.', 'Combine staying and switching for later rounds.',
'''Let `before[used][g]` be the best score after the rounds processed so far, using exactly `used` switches and ending with gesture g. In the code the gesture indices 0, 1 and 2 stand for H, P and S. After John's first H, Bessie's scores with zero switches are [0, 1, 0] for H, P and S. Exactly one switch is impossible after one round, because no pair of consecutive gestures exists yet.''',
table(['After round 0 (John: H)', 'End H', 'End P', 'End S'], [[f'used = {u}'] + ['–' if v is None else str(v) for v in LAYERS[0][u]] for u in range(2)]),
f'''An impossible state must be told apart from a possible state with zero wins. The code uses negative infinity, `-float('inf')`: adding 0 or 1 to it leaves it impossible, and it never wins a maximum. (A checked curiosity: on every game of up to five rounds with budgets up to 2, starting the impossible rows at 0 {"happens not to change" if ZERO_SAME else "changes"} the final answer, because a fake 0-win state is never better than a real strategy with fewer switches. But the table would then claim strategies that do not exist, so we keep the honest mark.)'''),
section('Stay with the gesture or change before this round', ['L5-07'], 'Compute a cell from its stay and switch predecessors, with every value shown.', 'Follow all five rounds.',
'''To compute a state for the current round, ask how its ending gesture was reached. Either Bessie kept that gesture: read the previous round with the same used count and the same gesture. Or she switched now: read the previous round with one fewer switch and a different gesture. Take the best available predecessor, then add this round's win.''',
figure(TRANS, f'Computing now[1][H] for round 2 of HHSSP: the best of one stay predecessor and two switch predecessors, plus the win for H against S. The result is {TRANS_VALUE}.'),
'''The switch count describes changes between Bessie's consecutive gestures, not changes in John's sequence: John may change without Bessie switching at all. A switch predecessor must have a different gesture; moving from H to H does not spend a switch.'''),
section('Follow all five rounds', ['L5-08'], 'Fill every cell of every round with the arithmetic written out.', 'Keep only the previous round in the program.',
'''Every cell of rounds 1 to 4 is worked below (– marks an impossible state; "not allowed" means there is no row used − 1).''',
table(work_head, WORK[:12], work_cols),
table(work_head, WORK[12:], work_cols),
'''The scores after each prefix of John's sequence, read from the table:''',
table(['After', '0: H', '0: P', '0: S', '1: H', '1: P', '1: S'], K.hps_prefix_table(J, 1)),
f'''The final zero-switch scores are [{', '.join(str(v) for v in LAYERS[-1][0])}] and the one-switch scores [{', '.join(str(v) for v in LAYERS[-1][1])}]. The answer is the largest score across both rows, {P.hps_table(J, 1)}. We include both rows because the budget is an upper limit, not a requirement to spend exactly one switch. Note on the last round that ending in S after one switch reaches 3 by switching from the zero-switch P strategy (2) and winning; we cannot take the four-win one-switch H strategy and switch again, because that would need two switches.'''),
)

ch3 = chapter('Keep only the previous round', 'Implement the same transition without retaining every round.',
section('Read before; write now', ['L5-09'], 'Read the program line by line and give its cost.', 'Test budgets that change the answer.',
'''The transition reads only the previous round. Use `before` for that completed round and a fresh `now` for the current one. For every used count and ending gesture, collect the candidates from before, add the current win and write the result into now. Replace before only after the whole new round is filled. Updating one table in place would let a later cell read a score already updated for this round, counting a round twice or spending several switches in one round.''',
code('hps_table', "print(hps_table('HHSSP', 1))"),
python(['enumerate', 'inf', 'listcomp', 'slice', 'int-bool', 'genexp', 'listmul'], 'enumerate, slices and the final max', '''`for g, gesture in enumerate(gestures):` gives both the index g (0, 1, 2) and the letter ('H', 'P', 'S'). `john[1:]` is a slice: every round except the first, which was handled on lines 9 to 10. `[[impossible] * 3 for _ in range(budget + 1)]` builds budget + 1 separate rows of three. The local name `best_before` holds the best predecessor score of one cell. `[impossible] * 3` is a row of three impossible scores. `max(max(row) for row in before)` uses a generator expression to find the largest score in any row; `int(…)` turns it into a whole number for printing.'''),
cost('Cost of hps_table, line by line (N rounds, budget K)', 'hps_table', ((J, 1), dict(N=5, K=1), 'Runs for HHSSP, K = 1'), (dict(N=100000, K=20), 'For N = 100,000, K = 20'),
     [('for opponent in john[1:]:', 'N − 1 rounds, plus the final check', lambda N, K: N),
      ('for used in range(budget + 1):', 'K + 2 per round', lambda N, K: (N - 1) * (K + 2)),
      ('best_before = before[used][g]', 'once per cell: 3(K + 1) per round', lambda N, K: (N - 1) * 3 * (K + 1)),
      ('if old != g:', 'three per cell with used ≥ 1', lambda N, K: (N - 1) * 9 * K),
      ('now[used][g] = best_before', 'once per cell', lambda N, K: (N - 1) * 3 * (K + 1))]),
f'''Each round fills 3(K + 1) cells and each cell looks at up to two switch predecessors: O(N × K) time, about eighteen million comparisons at full size, and O(K) memory for the two layers (the input needs its own O(N)). The full-size test took {T_HPS:.1f} s locally with CPython. The final maximum covers every used count from 0 to K; looking only at row K could reject an optimal strategy that needs fewer switches.'''),
section('Test budgets that change the answer, then ones that do not', ['L5-10', 'L5-11'], 'Check the difference between "exactly" and "at most" on small games.', 'Collect the edge cases, mistakes and the judge submission.',
table(['John', 'Budget', 'One best strategy', 'Switches', 'Wins'], [[j, str(k), *map(str, best_s(j, k))] for j, k in [('HPS', 0), ('HPS', 1), ('HPS', 2), ('HHH', 0), ('HHH', 2), ('S', 0), ('S', 2)]]),
'''For John = HPS no fixed gesture wins more than one round; one switch allows two wins and two switches all three. For HHH, budgets 0 and 2 both give 3 by keeping P; a larger allowance cannot make the optimum worse, but it need not improve it. The table keeps exact usage so transitions are precise; the final maximum over all usage counts enforces "at most". Budgets larger than the number of gaps between rounds leave some exact rows impossible, which is harmless.''',
pause('Why is it safe to discard a lower-scoring history only when its state fields match another history?', 'With the same round, used-switch count and ending gesture, both histories have identical legal continuations. If any field differs, the available choices or remaining budget may differ, so the score alone cannot decide which history is useful.')),
section('Hoof, Paper, Scissors: edge cases, mistakes and the judge', [], 'Prepare students to test the program and submit it to USACO.', 'Bring the five lessons together.',
edges([['One round, S, budget 2', str(P.hps_table('S', 2)), 'No switch is possible or needed.'],
       ['HHH, budget 0', str(P.hps_table('HHH', 0)), 'The first gesture is free: keep P.'],
       ['HHH, budget 2', str(P.hps_table('HHH', 2)), 'Exact-2 strategies win only 2; the answer must look at every row.'],
       ['HPS, budget 1', str(P.hps_table('HPS', 1)), 'A budget that changes the answer.'],
       ['100,000 rounds, budget 20', C(P.hps_table(FULLJ, 20)), 'Twenty-one constant runs: twenty switches win every round.']]),
mistakes([['return only row K', 'exactly K switches, not at most', K.variant('hps_table', 'return int(max(max(row) for row in before))', 'return int(max(before[budget]))', "hps_table('HHH', 2)") + ' on HHH, 2 (3)'],
          ['update one table in place', 'a round can use two switches', K.variant('hps_table', 'now = [[impossible] * 3 for _ in range(budget + 1)]', 'now = before', "hps_table('HH', 2)") + ' on HH, 2 (2)'],
          ['charge a switch for the first gesture', 'budget 0 allows nothing', K.variant('hps_cached', "change = int(previous != '' and gesture != previous)", 'change = int(gesture != previous)', "hps_cached('HHH', 0)") + ' on HHH, 0 (3)'],
          ['hps_cached on 5,000 rounds', 'a chain of 5,000 calls', K.variant('hps_cached', "return best(0, budget, '')", "return best(0, budget, '')", "hps_cached('H' * 5000, 2)")]]),
'''To submit, use the program below, exactly the file programs/hps_table.py. Like Fruit Feast, it reads hps.in and writes hps.out.''',
judge('hps_table'),
python(['open', 'with', 'read', 'split', 'map', 'write'], 'reading and writing files', '''`with open('hps.in') as source:` opens the input file and closes it when the block ends. `source.read().split()` gives every word of the file: the first two are N and K (`map(int, words[:2])` converts them), and `words[2:]` is the list of John's gestures. `open('hps.out', 'w')` opens the output file for writing, and `target.write(…)` writes the answer and a line ending.'''),
f'''Judge notes. `source.read().split()` reads every word of the file: N and K first, then the gestures, whatever the line breaks. The answer and a newline go to hps.out; printing to the screen gets no credit. The full-size test took {T_HPS:.1f} s locally with CPython. Do not submit the recursive version.''',
recap('The state is (round, switches used, ending gesture); the value is the most wins.',
      'now[used][g] = max(stay: before[used][g], switch: before[used − 1][other g]) + win; impossible states are −∞.',
      'Fill a fresh now from an untouched before; the answer is the maximum over every row 0 to K.',
      'O(N × K) time, O(K) memory.')),
section('Bring the five lessons together', ['L5-12'], 'Restate the main idea and compare the five lessons.', 'Use the practice files to test the program.',
table(['Lesson', 'Main idea', 'Stored answer', 'Combine with'], [['1', 'Remember the answer', 'route counts, cheapest costs', '+, min'], ['2', 'Count the ways to arrive', 'counts by last move', '+'], ['3', 'Remember the missing detail', 'costs and counts with an extra field', 'min, +'], ['4', 'Track what is possible', 'yes/no flags', 'mark'], ['5', 'Choose when to switch', 'maximum wins', 'max']], r'>{\raggedright\arraybackslash}p{12mm}XX>{\raggedright\arraybackslash}p{20mm}'),
'''That is this lesson's main idea: choose when to switch. Here the three state fields are justified by the round, the switch allowance and the gesture that decides whether the next choice costs a switch. Across the five lessons the stored answers have meant route counts, minimum costs, reachability flags and maximum scores, and the combining operation always followed the meaning. In a new problem, begin with a small instance, describe one subproblem in a full sentence, find the information that distinguishes its future, work out the legal ways to obtain its answer, fix the starting states and choose an order in which every required answer is ready. The table's shape comes after those decisions.'''),
)

appendix = [chapter('Summary tables', 'Reference tables for planning and for checking a student\'s claim quickly.',
section('Every algorithm in this lesson', [], 'Compare the cost of every program in one place.', 'Keep this page beside you while teaching.',
table(['Program', 'Time', 'Extra memory', 'Recursion depth', 'Use for'],
      [['hps_cached', 'O(N × K) states, 3 candidates each', 'O(N × K)', 'N', 'small examples'],
       ['hps_table', 'O(N × K)', 'O(K)', 'none', 'the judge']], r'>{\raggedright\arraybackslash}p{22mm}X>{\raggedright\arraybackslash}p{18mm}>{\raggedright\arraybackslash}p{18mm}X'),
'''Names: N = len(john), K = budget, `used` = switches already used, g = ending gesture (0, 1, 2 for H, P, S). The Python features explained in this book are dictionaries, int(True), looping over a string, @lru_cache, nested functions, max, enumerate, slices, list comprehensions and float('inf').'''),
section('Planning the two hours', [], 'See the lesson plan and what may move to the next meeting.', 'This is the end of the book; the teacher guide follows the same plan.',
table(['Minutes', 'Activity', 'Questions'], [[a, b, ('L5-' + c.replace('-', ' to L5-')) if c else ''] for a, b, c in __import__('content').LESSONS[4]['plan']], r'>{\raggedright\arraybackslash}p{16mm}X>{\raggedright\arraybackslash}p{26mm}'),
'''Writing hps_table (L5-09) is the hardest step of the course. Trace one full round of the table (section 2.4) before any code, and let students finish the program as follow-up work if the slot is too short.'''))]

BOOK = dict(
    idea='When a budget limits how often you may change your choice, keep in the state what each change depends on (switches used and the current gesture), compare staying with switching at every step, and take the best over every allowed amount of the budget.',
    intro='Hoof, Paper, Scissors combines the ideas of the earlier lessons. Bessie chooses a gesture for each round but may change it only a limited number of times. We first solve the game with no changes, then place a single switch by hand. That shows why a state must remember the round, the current gesture and the number of changes already used. We trace a small table in full before reducing the program to two consecutive rounds.',
    outcomes=['state Hoof, Paper, Scissors exactly and solve small games by hand;',
              'explain why the state needs the round, the switches used and the gesture;',
              'compute every cell of the table from its stay and switch predecessors;',
              'explain exactly versus at most, and why the answer looks at every row;',
              'give the cost of the program line by line and submit it to USACO with file input and output.'],
    front=['Read this book before the lesson. The separate teacher guide holds the short classroom prompts and answers; the margin notes here name the matching question IDs on the worksheet, slides and notebook. Every program is printed in full, and every number about running code (line counts, wrong outputs, timings) was produced by running the programs.',
           'Students need Lessons 1 to 4 and Python functions, lists, loops and dictionaries. Each new Python feature is explained in a grey PYTHON note beside the first program that uses it.',
           'Each section opens with its objective and ends by pointing to the next. The problem ends with its edge cases, common mistakes (with the wrong output each one produces), how to submit it and a recap. The example used throughout is John = HHSSP with budget 1. The summary tables and the two-hour plan are in the appendix.'],
    chapters=[ch1, ch2, ch3], appendix=appendix)
