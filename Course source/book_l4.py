"""Lesson 4 tutor book: Fruit Feast. Main idea: track what is possible."""
import inspect
import programs as P
import book_kit as K
import book_figures as F
from book_blocks import (section, chapter, code, diagram, table, pause, figure, python,
                         problem, items, recap, listing, judge, cost, edges, mistakes)

C = K.comma
EX = (10, 4, 7)
L10 = K.feast_layers(*EX)
L9 = K.feast_layers(9, 4, 6)
FULL = (5000000, 743782, 939000)
LFULL = K.feast_layers(*FULL)
T_FEAST = K.seconds(P.feast_table, FULL)
FEAST_SRC = inspect.getsource(P.feast_table)
CLIP = FEAST_SRC.replace('''                if fullness + fruit <= limit:
                    dry[fullness + fruit] = 1''', '''                dry[min(fullness + fruit, limit)] = 1''')
assert CLIP != FEAST_SRC
GREEDY = '''def feast(limit, a, b):
    reach = [False] * (limit + 1); reach[0] = True
    for f in range(limit + 1):
        if reach[f]:
            for x in (a, b):
                if f + x <= limit: reach[f + x] = True
    top = max(f for f in range(limit + 1) if reach[f])
    after = [False] * (limit + 1); after[top // 2] = True
    for f in range(limit + 1):
        if after[f]:
            for x in (a, b):
                if f + x <= limit: after[f + x] = True
    return max(top, max(f for f in range(limit + 1) if after[f]))
'''
MULTI = '''def feast(limit, a, b):
    reach = [False] * (limit + 1); reach[0] = True; changed = True
    while changed:
        changed = False
        for f in range(limit + 1):
            if reach[f]:
                for g in (f + a, f + b, f // 2):
                    if g <= limit and not reach[g]: reach[g] = changed = True
    return max(f for f in range(limit + 1) if reach[f])
'''
fruit_cols = r'>{\raggedright\arraybackslash}p{24mm}X'


def flags(head, rows):
    return table(head, rows, r'>{\raggedright\arraybackslash}p{17mm}' + 'X' * (len(head) - 1))

feast_problem = problem(
    name='Fruit Feast',
    story='Bessie the cow eats fruit, and may drink water once to make room for more.',
    rules='Bessie starts with fullness 0, and her fullness must never go above a limit. Eating an orange adds a to her fullness; eating a lemon adds b. There is as much of each fruit as she likes, and she may stop at any time. At most once, at any moment, she may drink water, which halves her fullness, rounding down: 7 becomes 3. A fruit that would take her above the limit cannot be eaten. What is the largest fullness she can reach? (The judge calls limit, a and b T, A and B.)',
    input='the file feast.in holds one line with limit, a and b.',
    output='write the largest fullness to the file feast.out.',
    limits='1 ≤ limit ≤ 5,000,000; 1 ≤ a, b ≤ limit. The problem page states no time limit.',
    example_in='8 5 6', example_out=str(P.feast_table(8, 5, 6)),
    why=f'Without water the best is {K.feast_from(0, 8, 5, 6)} (one lemon). With water: lemon (6), drink ({6 // 2}), orange ({6 // 2 + 5}). The classroom example used throughout this book is limit 10, a = 4, b = 7, with answer 10.',
    source='USACO 2015 December contest, Gold, problem 2.', url='http://www.usaco.org/index.php?page=viewproblem2&cpid=574')

ch1 = chapter('Find a legal sequence of actions', 'Understand the problem and tell a reachable fullness from one that merely lies below the limit.',
section('The Fruit Feast problem', ['L4-01'], 'State the problem exactly before solving it.', 'Explore the classroom example without water.',
'''This lesson has one main idea: track what is possible. Instead of counting routes (Lessons 1 to 3) or keeping a best value, we record for every situation a yes or no: can Bessie be here at all? The answer is then the largest situation marked yes.''',
feast_problem,
'''In this book limit is the largest permitted fullness, a the increase from one orange and b the increase from one lemon, exactly as in the code. The classroom example is limit 10, a = 4, b = 7.'''),
section('Eating without going over the limit', ['L4-01'], 'Find every fullness reachable without water, and see why 10 is not one of them.', 'Add the one drink of water.',
'''Without water, the reachable fullness values are 0, 4, 7 and 8: 4 by an orange, 7 by a lemon and 8 by two oranges. The table tries both fruits from each of them.''',
table(['Current fullness', 'Eat an orange (+4)', 'Eat a lemon (+7)'], [['0', '4: legal', '7: legal'], ['4', '8: legal', '11: forbidden (over 10)'], ['7', '11: forbidden', '14: forbidden'], ['8', '12: forbidden', '15: forbidden']]),
'''The answer without water is 8. It is not 10 merely because 10 lies inside the allowed range: a fullness is reachable only if some legal sequence of actions attains it. Eating a fruit that would exceed the limit is forbidden; we do not clip the result back to the limit.'''),
section('Water can make room for another fruit', ['L4-02'], 'Find the route that reaches 10, and see why "eat as much as possible, then drink" fails.', 'Find the detail that two situations with equal fullness can differ in.',
'''At most once, Bessie may drink water, which halves her fullness and rounds down. Python's integer division `// 2` expresses this: fullness 7 becomes 3, and fullness 8 becomes 4. With limit 10 and fruits 4 and 7: eat a lemon (7), drink (3), eat a lemon (10). Every intermediate fullness is within the limit, and 10 is the limit itself, so nothing larger is possible.''',
diagram('L4-02'),
'''There is a choice about when to drink. The table tries every reachable dry fullness as the moment to drink, then eats as much as possible afterwards.''',
table(['Drink at', 'After drinking', 'Best after more fruit'], [[str(f), f'{f} // 2 = {f // 2}', str(K.feast_from(f // 2, *EX))] for f in (0, 4, 7, 8)]),
'''Drinking immediately gives 0 again and wastes the drink. Drinking at 8, the largest dry value, gives 4, from which the best is 8. Drinking at 7 gives 3, which allows 10. So "eat as much as possible, then drink" can miss the best result: we must consider every reachable fullness as a moment to drink, not only the largest.''',
pause('Why does drinking from 7 help more than drinking from 8 in this example?', 'The rounded result from 7 is 3, and adding a lemon reaches 10. The rounded result from 8 is 4; adding 7 would exceed the limit, and adding 4 reaches only 8.')),
section('Same fullness, different future choices', ['L4-03'], 'Show that fullness alone is not a state, and introduce the dry and wet layers.', 'Search the states recursively.',
'''Fullness 4 can occur before drinking (one orange) and after drinking (two oranges to 8, then halve). The two situations have the same fullness but different futures: the first may still drink, the second may not. The state therefore needs both the fullness and whether the water has been used.

Picture two copies of the fullness numbers: a dry layer for states before drinking and a wet layer for states after. Eating stays within a layer and moves right. Drinking moves from the dry layer down to the wet layer, usually to the left. There is no move back up and no second drink.''',
figure(F.feast_layers(), 'The two layers for limit 10, fruits 4 and 7. The route 0 → 7 → 3 → 10 eats a lemon, drinks, then eats a lemon.'),
'''We store reachability: whether a state is possible. We do not count the routes to it. Two different routes to the same fullness with the same water status have exactly the same continuations, so one yes/no flag per state is enough.'''),
)

ch2 = chapter('From a recursive search to three passes', 'Choose an evaluation order that follows every dependency.',
section('A small recursive search', ['L4-04'], 'Write best(fullness, used_water) and see why it is only for small limits.', 'Mark the dry layer with one forward scan.',
'''Let best(fullness, used_water) be the greatest final fullness reachable from that state. Stopping now is always allowed, so the first candidate is the current fullness. Then try either fruit if it fits, staying in the same layer. Finally, if the water is unused, try the halved fullness with the water marked used. Eating strictly increases fullness, so within one layer there is no cycle; drinking can lower fullness but changes the water status, so it can never lead back to the same state.''',
code('feast_cached', 'print(feast_cached(10, 4, 7))'),
python(['decorator', 'nested', 'max', 'not', 'floordiv'], 'max, not and //', '''`max(answer, x)` keeps the larger of two values. `not used_water` is True while the water is still available. `fullness // 2` is integer division: it divides and rounds down, so `7 // 2` is 3. `@lru_cache(None)` (imported on line 1) remembers each (fullness, used_water) answer, and because `best` is nested inside `feast_cached`, each new feast starts with an empty cache.'''),
f'''The example visits {K.calls(P.feast_cached, EX, 'best')} states. At the full limit of 5,000,000 there can be millions of states and recursive chains thousands of calls deep (fruits of size 1 make a chain as long as the limit), so the iterative method stores compact flags instead. Note the change of meaning: the recursive function returns the best future fullness; the tables that follow record whether a state can be reached from the start.'''),
section('First pass: mark every fullness reachable before water', ['L4-05'], 'Fill dry[f] with one forward scan and explain why one scan suffices.', 'Drink from every reachable dry state.',
'''Let `dry[f]` be true when fullness f can be reached without drinking. Begin with only `dry[0]` true. Visit f from 0 upwards; whenever `dry[f]` is true, mark f + a and f + b if they do not exceed the limit.''',
table(['Reachable f', 'Moves tried'], L10['dry_rows'], fruit_cols),
flags(['f'] + [str(f) for f in range(EX[0] + 1)], [['dry[f]'] + K.yn(L10['dry'])]),
'''One forward scan suffices because every fruit adds a positive amount: a newly marked fullness is larger than its source, so the loop has not passed it yet, and when the loop reaches it, it propagates from it in turn.'''),
section('Second pass: drink from every reachable dry state', ['L4-06'], 'Seed the wet layer with every f // 2.', 'Eat again in the wet layer.',
'''Let `wet[f]` be true when fullness f can be reached after using the water. For every true dry entry, mark `wet[f // 2]`.''',
table(['Dry f', 'Wet seed'], L10['water_rows'], fruit_cols),
'''Water destinations may be smaller than their sources. That is why the water moves are made after the whole dry scan, not mixed into it: every dry source is then known, and all the wet seeds exist before any wet propagation begins. Several dry values can halve to the same wet value; marking a true flag again changes nothing. A "seed" is just a wet state reached directly by drinking, before any more fruit.'''),
section('Third pass: eat from the wet starting values', ['L4-07'], 'Propagate fruit through the wet layer and read off the answer.', 'Put the three passes into one program.',
'''Now scan the wet layer from 0 upwards with the same fruit moves. No water is offered in this pass: these states have already used it.''',
table(['Reachable wet f', 'Moves tried'], L10['wet_rows'], fruit_cols),
flags(['f'] + [str(f) for f in range(EX[0] + 1)], [['dry[f]'] + K.yn(L10['dry']), ['wet[f]'] + K.yn(L10['wet'])]),
f'''The answer is the largest fullness reachable in either layer: {L10['best']}. Checking both layers keeps the water optional: a best route may use no drink at all.'''),
section('The complete iterative program', ['L4-08'], 'Read the program pass by pass and give its cost line by line.', 'Check the method on a new feast.',
'''A bytearray stores small whole numbers compactly; we use 1 for reachable and 0 for unreachable. Both layers have limit + 1 entries, for fullness 0 up to the limit itself. The three passes are the dry scan, the water moves and the wet scan; a final backward search finds the largest reachable fullness and changes nothing.''',
code('feast_table', 'print(feast_table(10, 4, 7))'),
python(['bytearray', 'truthy', 'or', 'negstep'], 'bytearray, truth values and a backward range', '''`bytearray(limit + 1)` is a sequence of limit + 1 small integers, all 0, using one byte each: 5,000,001 entries take about 5 MB, where a list would take about 40 MB. `if dry[fullness]:` treats 0 as false and 1 as true. `range(limit, -1, -1)` counts down from the limit to 0, so the first reachable fullness found is the largest, and `return` ends the function at once.'''),
cost('Cost of feast_table, line by line', 'feast_table', (EX, dict(t=10, L=L10), 'Runs for (10, 4, 7)'), (dict(t=FULL[0], L=LFULL), 'For the large test'),
     [(('for fullness in range(limit + 1):', 1), 'pass 1: limit + 1 times, plus the final check', lambda t, L: t + 2),
      (('if dry[fullness]:', 1), 'once per fullness', lambda t, L: t + 1),
      ('dry[fullness + fruit] = 1', 'once per legal fruit move in the dry layer', lambda t, L: L['dry_moves']),
      ('wet[fullness // 2] = 1', 'once per reachable dry fullness', lambda t, L: L['D']),
      ('if wet[fullness]:', 'once per fullness', lambda t, L: t + 1),
      ('wet[fullness + fruit] = 1', 'once per legal fruit move in the wet layer', lambda t, L: L['wet_moves']),
      ('if dry[fullness] or wet[fullness]:', 'from the limit down to the answer', lambda t, L: t - L['best'] + 1)]),
f'''Three passes each visit limit + 1 entries with constant work per entry, followed by at most limit + 1 checks in the backward search: O(limit) time, not O(limit³). Their costs add because one scan finishes before the next starts. The two bytearrays use O(limit) memory. The large test (limit {C(FULL[0])}, fruits {C(FULL[1])} and {C(FULL[2])}) took {T_FEAST:.1f} s locally. The two fruit sizes are a fixed factor; with a list of k fruit sizes the work would be O(k × limit).'''),
)

ch3 = chapter('Check the method on a new feast', 'Separate a worked example from the reason the algorithm is correct.',
section('Try limit 9 and fruit sizes 4 and 6', ['L4-09'], 'Run the three passes on a new example and see which pass produced each value.', 'Test the boundary cases and the order of the passes.',
'''Listing the dry states, the immediate water destinations and the final wet states separately shows which pass produced each value.''',
flags(['f'] + [str(f) for f in range(10)], [['dry[f]'] + K.yn(L9['dry']), ['just drank'] + K.yn(K.feast_seeds(9, 4, 6)), ['wet[f]'] + K.yn(L9['wet'])]),
table(['Reachable wet f', 'Moves tried'], L9['wet_rows'], fruit_cols),
f'''A route to {L9['best']} is to eat 6, drink (3), then eat 6. The dry maximum was 8, so drinking improved the answer.'''),
section('Fruit Feast: edge cases, mistakes and the judge', ['L4-10', 'L4-11'], 'Test the boundaries, see the wrong outputs of common mistakes and submit to USACO.', 'Restate the main idea.',
edges([['(1, 1, 1)', str(P.feast_table(1, 1, 1)), 'Smallest input: one fruit reaches the limit.'],
       ['(8, 4, 6)', str(P.feast_table(8, 4, 6)), '4 + 4 reaches the limit without water.'],
       ['(5, 4, 4)', str(P.feast_table(5, 4, 4)), 'Water cannot help: drinking at 4 gives 2, and 2 + 4 > 5. A drink need not be used.'],
       ['(5, 3, 3)', str(P.feast_table(5, 3, 3)), 'Catches programs that allow two drinks (they reach 5).'],
       ['(10, 4, 7)', str(P.feast_table(*EX)), 'The best moment to drink is not at the largest dry value.'],
       [f'({C(FULL[0])}, {C(FULL[1])}, {C(FULL[2])})', C(P.feast_table(*FULL)), 'Full size; the answer is below the limit, so `return limit` fails.']]),
mistakes([['eat as much as possible, then drink', 'drinks only at the largest dry value', K.run_variant(GREEDY, 'feast(10, 4, 7)') + ' (10)'],
          ['clip to the limit: `dry[min(f + fruit, limit)]`', 'marks the limit even when no fruit fits exactly', K.run_variant(CLIP, 'feast_table(5, 3, 3)') + ' on (5, 3, 3) (4)'],
          ['one layer, water allowed any time', 'solves a problem with many drinks', K.run_variant(MULTI, 'feast(5, 3, 3)') + ' on (5, 3, 3) (4)'],
          ['`return limit`', 'ignores reachability', f'{C(FULL[0])} on the large test ({C(P.feast_table(*FULL))})'],
          ['feast_cached on (10,000, 1, 2)', 'a chain of thousands of calls', K.variant('feast_cached', 'return best(0, False)', 'return best(0, False)', 'feast_cached(10000, 1, 2)')]]),
'''The pass order works for every valid input for the same reason it works in the examples: every fruit edge moves to a larger fullness in the same layer, every water edge moves from dry to wet, and finishing all dry states, then all water edges, then all wet states visits every dependency before the states that need it.''',
pause('What goes wrong if wet states are allowed to drink again?', 'The program then solves a different problem with several drinks. A second halving may create fullness values that no legal one-drink route can reach: on (5, 3, 3) it reaches 5 instead of 4.'),
'''To submit, use the program below, exactly the file programs/feast_table.py. USACO problems of this period read from and write to named files, not the keyboard and screen.''',
judge('feast_table'),
python(['open', 'with', 'read', 'split', 'map', 'write'], 'reading and writing files', '''`open('feast.in')` opens the input file for reading; `with … as source:` closes it automatically when the block ends. `source.read().split()` reads the whole file and cuts it into words, and `map(int, …)` converts the three words to numbers. `open('feast.out', 'w')` opens the output file for writing (creating or emptying it), and `target.write(str(answer) + '\\n')` writes the answer and a line ending.'''),
f'''Judge notes. The program opens feast.in, reads the three numbers, and writes the answer and a newline to feast.out; printing to the screen instead gets no credit. `with open(…) as source:` closes the file automatically. Python is accepted; the full-size test took {T_FEAST:.1f} s locally. Do not submit the recursive version.''',
recap('A state is (fullness, water used); its value is yes or no: can Bessie be there?',
      'Pass 1 marks the dry layer forwards; pass 2 drinks from every dry state; pass 3 marks the wet layer forwards.',
      'The answer is the largest fullness marked in either layer; never clip to the limit.',
      'O(limit) time and memory with two bytearrays.')),
section('Why the water status is part of the state', ['L4-11'], 'Restate the main idea and why the extra dimension restores a forward order.', 'Use the practice files to test the program.',
'''That is the main idea of the lesson: track what is possible. The water-status field separates two situations that have different legal futures. Once they are separated, the backward-looking move caused by halving no longer prevents a forward order: inside each layer every move goes right, and the only move between layers goes from dry to wet. Adding a dimension to a state is justified by exactly this kind of difference in the future, never by a wish for a bigger table.'''),
)

appendix = [chapter('Summary tables', 'Reference tables for planning and for checking a student\'s claim quickly.',
section('Every algorithm in this lesson', [], 'Compare the cost of every program in one place.', 'Keep this page beside you while teaching.',
table(['Program', 'Time', 'Extra memory', 'Recursion depth', 'Use for'],
      [['feast_cached', 'O(limit) states', 'O(limit)', 'up to limit', 'small examples'],
       ['feast_table', 'O(limit): three passes and a backward search', 'two bytearrays of limit + 1 bytes', 'none', 'the judge']], r'>{\raggedright\arraybackslash}p{24mm}X>{\raggedright\arraybackslash}p{26mm}>{\raggedright\arraybackslash}p{18mm}X'),
'''Names: `dry[f]` (reachable without water, "no drink" on the worksheet) and `wet[f]` (reachable after the drink, "after water"); the judge's T, A and B are our limit, a and b. The Python features explained in this book are @lru_cache, nested functions, max, not, //, bytearray, truth values of 0 and 1, or, range with step −1 and reading and writing files with open.'''),
section('Planning the two hours', [], 'See the lesson plan and what may move to the next meeting.', 'This is the end of the book; the teacher guide follows the same plan.',
table(['Minutes', 'Activity', 'Questions'], [[a, b, ('L4-' + c.replace('-', ' to L4-')) if c else ''] for a, b, c in __import__('content').LESSONS[3]['plan']], r'>{\raggedright\arraybackslash}p{16mm}X>{\raggedright\arraybackslash}p{26mm}'),
'''Draw the two-layer picture (section 1.4) on the board before any code: it carries the whole lesson. If time is short, L4-09 can be finished as homework with the local test files.'''))]

BOOK = dict(
    idea='When the question is "what can happen?", store a yes or no for every situation, add to the situation whatever changes its future (here: has the water been used?), and choose an order in which every move goes forward.',
    intro='Fruit Feast asks which fullness values can be reached without exceeding a limit. We first explore a tiny instance by hand. Water then gives two situations with the same fullness but different future choices. That observation leads to two layers of states and, finally, three simple forward passes. The layers enforce the one-drink rule while still considering every useful moment to drink.',
    outcomes=['state Fruit Feast exactly and find the reachable fullness values of a small case by hand;',
              'explain why fullness alone is not a state, and draw the dry and wet layers;',
              'run the three passes with every mark written out;',
              'give the cost of the program line by line and explain why three passes are O(limit);',
              'test the boundary cases and submit the program to USACO with file input and output.'],
    front=['Read this book before the lesson. The separate teacher guide holds the short classroom prompts and answers; the margin notes here name the matching question IDs on the worksheet, slides and notebook. Every program is printed in full, and every number about running code (line counts, wrong outputs, timings) was produced by running the programs.',
           'Students need Lessons 1 to 3 (states, recurrences, tables filled in order) and Python functions, lists and loops. Each new Python feature is explained in a grey PYTHON note beside the first program that uses it.',
           'Each section opens with its objective and ends by pointing to the next. The problem ends with its edge cases, common mistakes (with the wrong output each one produces), how to submit it and a recap. The summary tables and the two-hour plan are in the appendix.'],
    chapters=[ch1, ch2, ch3], appendix=appendix)
