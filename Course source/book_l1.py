"""Lesson 1 tutor book: Staircase and Frog. Main idea: remember the answer."""
import programs as P
from book_recursion import INTRO
import book_kit as K
import book_figures as F
from book_blocks import (section, chapter, code, diagram, table, pause, figure, python,
                         problem, items, recap, listing, judge, cost, edges, mistakes)

C = K.comma
H6 = [20, 50, 30, 40, 10, 10]
TREE, TREE_CALLS, TREE_REPEATS, TREE_DISTINCT = F.stairs_call_tree(5)
STACK, STACK_FRAMES = F.call_stack(5)
STONES, BEST_ROUTE, BEST_COST, GREEDY_ROUTE, GREEDY_COST = F.frog_routes(H6)
CALLS = [(n, K.calls(P.stairs_slow, (n,)), K.calls(P.stairs_cached, (n,), 'ways')) for n in (5, 10, 20, 30)]
FROG_CALLS = [(s, K.calls(P.frog_slow, (list(range(s)),), 'cost'), K.calls(P.frog_cached, (list(range(s)),), 'cost')) for s in (6, 10, 20, 30)]
BIG = P.stairs_table(10000)
T_FROG = K.seconds(P.frog_table, ([(i * 7919) % 10000 + 1 for i in range(100000)],), 3)
T_STAIRS = K.seconds(P.stairs_table, (10000,), 3)
greedy_rows = []
K.frog_greedy(H6, greedy_rows)
LINE6 = K.listing_line('stairs_slow', 'return stairs_slow(n - 1)')
LINE7 = K.listing_line('stairs_cached', 'cache[step] = ways(')

staircase_problem = problem(
    name='Staircase',
    story='You stand on the ground below a staircase and climb it by single or double steps.',
    rules='The ground is step 0. Each move climbs exactly 1 step or exactly 2 steps. A route is the ordered list of moves; [1, 2] and [2, 1] are different routes. Count the routes that land exactly on step n. In the variation (L1-13) the moves are 1 or 3 instead.',
    input='one line holding the target step n.',
    output='the exact number of routes (no remainder is taken; Python integers have no size limit).',
    limits='in our practice files 0 ≤ n ≤ 10,000; the answer for 10,000 has ' + C(len(str(BIG))) + ' digits.',
    example_in='5', example_out='8',
    why='The eight routes are 11111, 1112, 1121, 1211, 2111, 122, 212 and 221.',
    source='an original teaching exercise for this course; there is no online judge, so students test it with the local files.')

frog_problem = problem(
    name='Frog 1',
    story='A frog hops along a row of stones, and every hop costs effort.',
    rules='There are n stones in a row, numbered 0 to n − 1 in our programs (the judge numbers them from 1). Stone i has height heights[i]. The frog starts on stone 0 and must reach the last stone. From stone i it may jump to stone i + 1 or stone i + 2. A jump costs the difference between the two heights, ignoring the sign: from height 50 to 30 costs 20, and from 30 to 50 also costs 20. Find the smallest possible total cost.',
    input='the first line holds n; the second holds the n heights.',
    output='one integer: the smallest total cost.',
    limits='2 ≤ n ≤ 100,000; every height is from 1 to 10,000. The judge allows 2 seconds and 1024 MiB.',
    example_in='6\n20 50 30 40 10 10', example_out=str(P.frog_table(H6)),
    why=f'Jump 0 → 2 → 4 → 5: the costs are |30 − 20| = 10, |10 − 30| = 20 and |10 − 10| = 0, {BEST_COST} in all. No route is cheaper.',
    source='AtCoder, Educational DP Contest, problem A.', url='https://atcoder.jp/contests/dp/tasks/dp_a')

ch1 = chapter('Staircase: start with routes we can see', 'Understand the staircase problem and why its answer is a sum, before writing any code.',
section('The staircase problem', ['L1-05'], 'State the problem exactly: what is counted, what the input is and what the answer must be.', 'List the routes for small targets by hand.',
'''This lesson has one main idea: remember the answer to a question so that it is never worked out twice. We meet it first in a counting problem small enough to do by hand.''',
staircase_problem,
'''We are counting ordered lists of moves. A route written as [1, 2, 2] visits steps 1, 3 and 5; [2, 1, 2] visits steps 2, 3 and 5. Both finish at step 5, but they are different routes because their moves occur in a different order. To save space we write a route as its digits: 122 means [1, 2, 2].'''),
section('Five steps, eight routes', ['L1-05'], 'Build the complete list of routes for targets 1 to 5 and notice how the counts grow.', 'Find a way to organise the routes so that none is missed or counted twice.',
'''For the first step there is only 1. For the second there are 11 and 2. For the third there are 111, 12 and 21. Continue drawing before looking for a formula.''',
table(['Target step', 'Routes (122 means [1, 2, 2])', 'Count'], [[str(t), ', '.join(''.join(map(str, r)) for r in sorted(K.stairs_routes(t), key=lambda r: (-len(r), r))), str(len(K.stairs_routes(t)))] for t in range(1, 6)], r'>{\raggedright\arraybackslash}p{20mm}X>{\raggedright\arraybackslash}p{12mm}'),
'''Each digit in the table represents one move. The target step is a position; the number of routes is the answer stored for that position. Step 4 has five routes; the fact that its position is 4 does not make the answer 4.

At the board, let students build the first few rows themselves. The useful question is how to know that a list of routes is complete.'''),
section('Look at the final move', ['L1-06'], 'Explain why the count for step 5 is the count for step 4 plus the count for step 3.', 'Turn the rule into a function and give it somewhere to stop.',
'''A route reaching step 5 must end with a jump of 1 from step 4 or a jump of 2 from step 3. There is no other possible last move. We already know five routes to step 4. Append a jump of 1 to each of them: that gives five routes to step 5. Likewise, append a jump of 2 to each of the three routes to step 3: that gives three more.''', diagram('L1-06'),
'''These two groups cannot overlap: every route in the first group ends in 1 and every route in the second ends in 2. Together they include every legal route. This is why we add 5 and 3, obtaining 8. The addition follows from a partition of the routes, not just from spotting a pattern in the numbers.''',
table(['Last move', 'Earlier step', 'Routes there', 'Routes to step 5 in this group'], [['1', '4', '5', '11111, 1121, 1211, 2111, 221'], ['2', '3', '3', '1112, 122, 212'], ['Total', '', '5 + 3 = 8', 'all eight, each exactly once']]),
'''Now name the question. Let ways(n) be the number of routes from the ground to step n. Its argument n identifies the target step; its value counts routes. For a positive target the same last-move reasoning gives ways(n) = ways(n − 1) + ways(n − 2). A rule expressing an answer using answers to smaller questions is called a recurrence. "Smaller" refers to the target step; the recursive calls return route counts, not step numbers.'''),
section('Give the recursion somewhere to stop', ['L1-07', 'L1-08'], 'Choose the stopping cases ways(0) = 1 and ways(−1) = 0, then write and trace the first program.', 'Count how many calls this program makes, and why.',
'''A function cannot keep asking smaller questions for ever. At step 0 there is exactly one route: make no moves. This empty route is needed when we build a route consisting of one final jump: the one-jump route [2] is the empty route to step 0 followed by 2.

A negative target has no routes because every allowed jump moves upward. Thus ways(0) is 1 and ways(−1) is 0, and the recurrence gives ways(1) = ways(0) + ways(−1) = 1 + 0 = 1.

The first program translates that explanation directly. In code the function is called `stairs_slow`; `stairs_slow(n)` computes ways(n).''', code('stairs_slow', 'print(stairs_slow(5))'),
python(['def', 'recursion'], 'functions that call themselves', '''`def stairs_slow(n):` defines a function with one parameter, n. `return` hands a value back to whoever called the function and ends the call at once, so line 3 ends the call for a negative n before line 6 is reached. A function may call itself (line 6): each call is a separate question with its own n. Python pauses the calling line until the smaller call returns its number, then continues the addition.'''),
'''The table traces `stairs_slow(3)` in the order Python makes the calls. Each dot of indentation is one level deeper. A call returns its number to the call waiting for it; it does not jump the program straight to the final answer.''',
table(['Order', 'Call', 'What it asks', 'Returns'], K.stairs_slow_trace(3), r'>{\raggedright\arraybackslash}p{10mm}>{\raggedright\arraybackslash}p{36mm}X>{\raggedright\arraybackslash}p{14mm}'),
'''Notice that `stairs_slow(1)` is computed twice (calls 3 and 7) and `stairs_slow(0)` three times. That waste is the subject of the next chapter.'''),
)

ch2 = chapter('Remember an answer, then choose the order', 'Remove repeated computation with a cache, then remove deep recursion with a loop.',
section('A tree contains repeated questions', ['L1-09'], 'See, and count, the repeated calls that make the first program slow.', 'Save each answer the first time it is computed.',
f'''The call for target 5 asks about targets 4 and 3. The call for target 4 also asks about target 3. Those two calls for target 3 have exactly the same meaning: count routes from the ground to step 3 under the same rules. Repeating the calculation cannot change its answer. The picture shows every call that `stairs_slow(5)` makes.''',
figure(TREE, f'The complete call tree of stairs_slow(5). Each circle is one call; the number is its argument k. There are {TREE_CALLS} calls but only {TREE_DISTINCT} different arguments (−1 to 5); the {TREE_REPEATS} shaded calls repeat a question that was already asked earlier.'),
f'''Separate nodes show separate calls, even when they have the same label. If we joined all calls with the same argument into one node, only {TREE_DISTINCT} questions would remain. The table shows how quickly the number of calls grows. Every count was measured by running the program.''',
table(['Target n', 'Calls made by stairs_slow(n)', 'Different questions (−1 to n)', 'Calls made by the cached version'], [[str(n), C(a), str(n + 2), C(b)] for n, a, b in CALLS]),
f'''Each call of `stairs_slow` with n ≥ 1 runs line {LINE6}, which makes two more calls. The number of calls therefore satisfies calls(n) = 1 + calls(n − 1) + calls(n − 2); it is 2 × F(n + 2) − 1, where F is the Fibonacci sequence 0, 1, 1, 2, 3, 5, … . Each extra step multiplies the work by about 1.6, so the growth is exponential: target 30 already needs {C(CALLS[-1][1])} calls.''',
cost('Cost of stairs_slow, line by line', 'stairs_slow', ((30,), dict(n=30), 'Runs for n = 30'), (dict(n=10000), 'For n = 10,000'),
     [('if n < 0:', 'once per call', lambda n: 2 * K.fib(n + 2) - 1),
      ('return stairs_slow(n - 1) + stairs_slow(n - 2)', 'once per call with n ≥ 1, making two calls', lambda n: K.fib(n + 2) - 1)]),
f'''The longest chain of calls, by contrast, grows only linearly: {', '.join(map(str, range(5, -1, -1)))} is {len(range(5, -1, -1))} calls deep. Number of calls and depth of calls are different measurements. Caching addresses the first; iteration will address the second.'''),
section('Use the target step as the cache key', ['L1-10'], 'Store each answer in a dictionary under the target step, and see the call count fall to 2n + 1.', 'Find out why a cached recursion can still fail on a large target.',
'''A cache is a dictionary that remembers a result under the question that produced it. Here the whole question is identified by the target step: the ground, the allowed jumps and the counting rule never change, so no other information is needed in the key. For example, `cache[3] = 3` says that target step 3 has three routes. The key is the step number; the stored value is a route count.''',
code('stairs_cached', 'print(stairs_cached(5))'),
python(['nested', 'dict'], 'a function inside a function; dictionaries', '''`ways` is defined inside `stairs_cached` (lines 3 to 8). A nested function can read the variables of the function around it, so every call of `ways` shares the one dictionary `cache` created on line 2, and a fresh dictionary is made for each new top-level call. `{0: 1}` is a dictionary with key 0 and value 1. `step not in cache` (line 6) asks whether the key is missing; `cache[step] = …` stores a value under a key and `cache[step]` reads it back.'''),
f'''A missing key triggers the two smaller questions and the addition on line {LINE7}. A present key skips them. Each target from 1 to n is computed once, and each computation asks two questions, so `ways` is called 2n + 1 times in total.''',
cost('Cost of stairs_cached, line by line', 'stairs_cached', ((20,), dict(n=20), 'Runs for n = 20'), (dict(n=10000), 'For n = 10,000'),
     [('if step < 0:', 'once per call of ways', lambda n: 2 * n + 1),
      ('if step not in cache:', 'once per call with step ≥ 0', lambda n: 2 * n),
      ('cache[step] = ways(step - 1) + ways(step - 2)', 'once per new step 1 to n', lambda n: n)]),
'''So the work is O(n): it grows in proportion to the number of target steps, up to a constant factor. For staircase we keep exact counts, which become very large integers, and adding two numbers with thousands of digits costs more than adding two small ones. O(n) here counts additions, not microseconds.'''),
section('Why a cache does not prevent a recursion error', ['L1-11'], 'Picture the call stack and explain why caching does not make it shorter.', 'Fill the same answers with a loop, which needs no stack of waiting calls.',
'''Computing a new answer for target n calls target n − 1, which calls n − 2, and so on down to 0. Each unfinished call needs a stack frame: a record of its arguments and of the line where it must resume. The picture shows the stack of `stairs_cached(5)` at its deepest moment.''',
figure(STACK, f'The call stack of stairs_cached(5) at its deepest point: {STACK_FRAMES} frames are open at once. For target n there are n + 2 frames, however good the cache is.'),
'''Python limits this nesting depth, by default to about 1,000 frames. A cached recursive program can reach that limit long before its total work becomes expensive. The demonstration below asks for more nested calls than the current limit allows and catches the error, so the notebook keeps running.''',
code('recursion_demo', 'print(recursion_demo())'),
python(['import', 'try'], 'import, try and except', '''`import sys` (line 1) makes Python's system module available; `sys.getrecursionlimit()` reads the current depth limit instead of assuming a value. `try:` runs a block; if that block raises a `RecursionError`, Python jumps to the matching `except` block instead of stopping the program. If no error happens, the function reaches its last line and says so.'''),
'''Raising the recursion limit is not the lesson's solution. We already know which smaller answers every target needs, so we can compute them in an order that needs no waiting calls.'''),
section('Fill the table from the ground upward', ['L1-12'], 'Fill ways[0..n] with a loop in increasing order and explain each line of the program.', 'Change the allowed jumps and keep the same reasoning.',
'''Let `ways[step]` store the number of routes to the position called step. Begin with `ways[0] = 1`. To fill step 1, read step 0. To fill step 2, read steps 1 and 0. Continue upward: every entry we need has already been filled.''',
table(['Step', 'Reads', 'Arithmetic', 'ways[step]'], K.stairs_fill(5)),
'''The list is a cache whose filling order we choose. In the recursive version the requests decide when a missing answer is computed; here the loop visits the targets in increasing order. Both use the same recurrence.''',
code('stairs_table', 'print(stairs_table(5))'),
python(['listmul', 'range', 'augassign', 'negindex'], 'lists, range and +=', '''`[0] * (n + 1)` builds a list of n + 1 zeros, positions 0 to n. `range(1, n + 1)` produces 1, 2, …, n: the second number is excluded, so we write n + 1 to include the target. `ways[step] += x` means `ways[step] = ways[step] + x`. A negative index counts from the end of a list: `ways[-1]` is the last entry, not "step −1". That is why line 6 checks `step >= 2` before reading `ways[step - 2]`.'''),
cost('Cost of stairs_table, line by line', 'stairs_table', ((5,), dict(n=5), 'Runs for n = 5'), (dict(n=10000), 'For n = 10,000'),
     [('for step in range(1, n + 1):', 'n times, plus the final check that ends the loop', lambda n: n + 1),
      ('ways[step] = ways[step - 1]', 'once per step', lambda n: n),
      ('ways[step] += ways[step - 2]', 'once per step from 2 to n', lambda n: n - 1)]),
f'''The loop makes at most two additions per step and stores n + 1 answers: O(n) time and O(n) memory, with no recursion at all. On a laptop `stairs_table(10000)` takes about {T_STAIRS*1000:.0f} ms and returns a {C(len(str(BIG)))}-digit number.'''),
section('Change the jumps, keep the reasoning', ['L1-13'], 'Adapt the recurrence and the loop to jumps of 1 or 3.', 'Collect the staircase edge cases, mistakes and tests.',
'''Now allow jumps of 1 or 3. A route to step n ends at step n − 1 before a jump of 1, or at step n − 3 before a jump of 3. The ground still has one empty route. The allowed predecessors change, but the meaning of each stored answer stays the same.''',
table(['Step', 'Reads', 'Arithmetic', 'ways[step]'], K.stairs_fill(7, (1, 3))),
'''Step 5 uses the three routes to step 4 and the one route to step 2. This is a useful exercise because copying the old numbers fails, while reusing the last-move argument succeeds.''', code('stairs_13', 'print([stairs_13(n) for n in range(6)])'),
python(['tuple', 'listcomp'], 'looping over a tuple; building a list', '''`for jump in (1, 3):` runs the body once with jump = 1 and once with jump = 3; `(1, 3)` is a tuple, a fixed list of values. In the test line, `[stairs_13(n) for n in range(6)]` is a list comprehension: it calls the function for n = 0 to 5 and collects the six answers in a list.'''),
cost('Cost of stairs_13, line by line', 'stairs_13', ((8,), dict(n=8), 'Runs for n = 8'), (dict(n=10000), 'For n = 10,000'),
     [('for jump in (1, 3):', 'three checks per step (two jumps, then the end)', lambda n: 3 * n),
      ('if step >= jump:', 'twice per step', lambda n: 2 * n),
      ('ways[step] += ways[step - jump]', 'twice per step, except jump 3 at steps 1 and 2', lambda n: 2 * n - 2)]),
'''The same form will reappear with six possible final values in the dice problem of Lesson 2.'''),
section('Staircase: edge cases, mistakes and testing', [], 'Know the cases that break careless programs and the wrong outputs they produce.', 'Move to Frog, where the stored answers are costs instead of counts.',
edges([['n = 0', '1', 'The empty route. Returning 0 here makes every later count 0.'],
       ['n = 1', '1', 'Only one predecessor exists; a program that reads ways[n − 2] without a check reads ways[−1].'],
       ['n = 2', '2', 'The first step where both jumps are possible (11 and 2).'],
       ['Jumps 1 or 3, n = 2', str(P.stairs_13(2)), 'A jump of 3 overshoots; only 11 fits.'],
       ['n = 10,000', f'{C(len(str(BIG)))} digits', 'Exact big integers; recursion would exceed the depth limit.']]),
mistakes([['`ways[0] = 0` instead of 1', 'loses the empty route, so nothing is ever added', K.variant('stairs_table', 'ways[0] = 1', 'ways[0] = 0', 'stairs_table(5)') + ' (8)'],
          ['`range(1, n)` instead of `range(1, n + 1)`', 'never fills the target step', K.variant('stairs_table', 'range(1, n + 1)', 'range(1, n)', 'stairs_table(5)') + ' (8)'],
          ['no `step >= 2` check', 'step 1 reads ways[−1], the last entry; harmless for n = 5 but wrong for n = 1', K.variant('stairs_table', 'if step >= 2:', 'if True:', 'stairs_table(1)') + ' for n = 1 (1)'],
          ['no `n < 0` case in stairs_slow', 'stairs_slow(1) asks for −1, −2, −3, … for ever', K.variant('stairs_slow', '    if n < 0:\n        return 0\n', '', 'stairs_slow(3)')],
          ['`range(1, 4)` for jumps 1 or 3', 'also allows the forbidden jump of 2', K.variant('stairs_13', 'for jump in (1, 3):', 'for jump in range(1, 4):', 'stairs_13(7)') + ' for n = 7 (9)'],
          ['the cache created inside `ways`', 'each call gets an empty dictionary, so nothing is shared', 'right answer, slow']]),
'''Staircase is our own exercise, so there is no online judge. Students test `stairs_table` and `stairs_13` with the local files (`python3 starter.py`), described in the last chapter.''',
recap('ways(n) counts routes to step n; it is the sum over the possible last moves.',
      'ways(0) = 1 (the empty route); negative targets have 0 routes.',
      f'The plain recursion repeats questions: {C(CALLS[-1][1])} calls for n = 30.',
      'A cache keyed by the step computes each answer once: O(n) work, but still about n waiting calls.',
      'A loop in increasing order needs neither repeated work nor a deep stack.')),
)

ch3 = chapter('Frog: keep the cheapest route', 'Reuse the same ideas when the stored answers are costs, combined with min instead of +.',
section('The Frog problem', ['L1-14'], 'State the Frog problem exactly before solving it.', 'Compare whole-route costs on a small example.',
frog_problem,
'''We number stones from 0 so that stone i matches the Python list position `heights[i]`. The judge numbers them from 1; only the labels change.'''),
section('A route has a total cost', ['L1-14', 'L1-15'], 'Add up complete routes, and see why choosing the cheapest next jump fails.', 'Ask about the last jump into a stone, as we did for the staircase.',
'''With heights [10, 20, 30] the route 0, 1, 2 costs 10 + 10 = 20, and the direct jump 0, 2 also costs 20: fewer jumps do not necessarily mean a cheaper route. Now take the six stones of the judge's example. The picture shows them as columns of their heights.''',
figure(STONES, f'Heights {H6}. Above: the best route {"-".join(map(str, BEST_ROUTE))} with its jump costs (total {BEST_COST}). Below, dashed: the greedy route {"-".join(map(str, GREEDY_ROUTE))} (total {GREEDY_COST}).'),
'''A tempting rule is always to take the cheaper next jump, choosing the farther stone on a tie. The table follows that rule from stone 0.''',
table(['At stone', 'Next jumps', 'Greedy goes to', 'Total so far'], greedy_rows, r'>{\raggedright\arraybackslash}p{14mm}X>{\raggedright\arraybackslash}p{18mm}>{\raggedright\arraybackslash}p{16mm}'),
f'''Greedy pays {GREEDY_COST}. With only six stones we can list every route and its cost; brute force, unlike greedy, looks at all of them.''',
table(['Route', 'Jump costs', 'Total'], [['-'.join(map(str, r)), ' + '.join(map(str, c)), str(t)] for r, c, t in K.frog_all_routes(H6)]),
f'''The cheapest is {"-".join(map(str, BEST_ROUTE))} at {BEST_COST}: paying 20 rather than 10 for the jump from stone 2 leaves a free final jump. A choice that looks best for the next jump need not be best for the whole route. We need a method that compares complete costs without listing every route, because a row of n stones has about 1.6ⁿ routes.'''),
section('Ask about the last jump to a stone', ['L1-16'], 'Define cost(i), write its recurrence and the exhaustive recursive program.', 'Save each stone\'s answer, exactly as for the staircase.',
'''Let cost(i) mean the cheapest total cost from stone 0 to stone i. The argument i is a stone index; `heights[i]` is a height; cost(i) is a route cost. These three quantities are not interchangeable.

The last jump into stone i comes from stone i − 1 or, if it exists, stone i − 2. For each possible predecessor we need its cheapest route cost plus the cost of the final jump; then we choose the smaller total:''',
table(['Case', 'cost(i)'], [['i = 0', '0 (no jump is needed)'], ['i = 1', 'cost(0) + |heights[1] − heights[0]|'], ['i ≥ 2', 'min( cost(i − 1) + |heights[i] − heights[i − 1]|,  cost(i − 2) + |heights[i] − heights[i − 2]| )']], r'>{\raggedright\arraybackslash}p{16mm}X'),
'''Comparing only the two jump costs would ignore the cost of reaching their starting stones. The recursive program spells out the three cases.''', code('frog_slow', 'print(frog_slow([20, 50, 30, 40, 10, 10]))'),
python(['abs', 'min', 'len'], 'abs, min and len', '''`abs(x)` is the size of x without its sign, so `abs(30 - 50)` is 20. `min(one, two)` returns the smaller of its arguments. `len(heights)` is the number of stones, so `len(heights) - 1` is the index of the last stone.'''),
'''This exhaustive recursion is correct for every input it can finish. It is slow because each call makes two more, just like `stairs_slow`:''',
table(['Stones', 'Calls of cost in frog_slow', 'Calls in frog_cached'], [[str(s), C(a), C(b)] for s, a, b in FROG_CALLS]),
f'''For s stones frog_slow makes F(s + 2) − 1 calls ({C(FROG_CALLS[-1][1])} for 30 stones). On the judge's 100,000 stones it would also exceed Python's recursion limit long before it finished: the first chain of calls is 100,000 deep.'''),
section('The same stone asks the same question', ['L1-17'], 'Cache cost(i) by the stone index and explain why that is safe.', 'Fill the costs in a table from left to right.',
'''Several larger calls need the cheapest cost to stone 3. Every one of them refers to the same fixed height list and the same starting stone, so the answer can be saved under the key 3. We do not need to remember the route by which a call happened to ask: the state means the cheapest cost from the start to that stone over all legal routes.''', code('frog_cached', 'print(frog_cached([20, 50, 30, 40, 10, 10]))'),
cost('Cost of frog_cached, line by line (s = number of stones)', 'frog_cached', ((list(range(10)),), dict(s=10), 'Runs for s = 10'), (dict(s=100000), 'For s = 100,000'),
     [('if i not in cache:', 'once per call of cost', lambda s: 2 * s - 2),
      ('one = cost(i - 1)', 'once per stone 1 to s − 1', lambda s: s - 1),
      ('two = cost(i - 2)', 'once per stone 2 to s − 1', lambda s: s - 2)]),
'''Each stone is solved once with at most two candidates: O(n) time and O(n) memory. The chain of waiting calls is still about n long, so for 100,000 stones we need a loop.'''),
section('Work through the cost table', ['L1-18', 'L1-19'], 'Fill best[i] from left to right with the arithmetic written out, then implement it.', 'Collect the Frog edge cases, mistakes and the judge submission.',
'''Use `best[i]` for the cheapest cost to stone i. Fill the list from left to right, because both predecessors of a stone have smaller indices. The table works through the six-stone example.''',
table(['Stone i', 'Height', 'From i − 1', 'From i − 2', 'best[i]'], K.frog_fill(H6), r'>{\raggedright\arraybackslash}p{11mm}>{\raggedright\arraybackslash}p{11mm}XX>{\raggedright\arraybackslash}p{12mm}'),
'''Look at stone 4: coming from stone 3 costs 50, coming from stone 2 costs 30, and we store 30. That entry is a total route cost, not the cost of the last jump alone. The final jump from stone 4 costs 0 because the heights are equal; zero is a legitimate cost, not a forbidden jump.''',
code('frog_table', 'print(frog_table([20, 50, 30, 40, 10, 10]))'),
python(['negindex'], 'best[-1]', '''`best[-1]` is the last entry of the list, the cheapest cost to the final stone. Writing `best[len(heights) - 1]` would mean the same.'''),
cost('Cost of frog_table, line by line (s = number of stones)', 'frog_table', ((list(range(10)),), dict(s=10), 'Runs for s = 10'), (dict(s=100000), 'For s = 100,000'),
     [('for i in range(1, len(heights)):', 's − 1 times, plus the final check', lambda s: s),
      ('best[i] = best[i - 1]', 'once per stone 1 to s − 1', lambda s: s - 1),
      ('two = best[i - 2]', 'once per stone 2 to s − 1', lambda s: s - 2)]),
pause('For heights [10, 30, 20, 40], fill the entire best list before running the function.', 'The table below gives [' + ', '.join(r[-1] for r in K.frog_fill([10, 30, 20, 40])) + ']. Routes 0, 1, 3 and 0, 2, 3 both cost 30. The task asks for the cheapest cost, so ties do not create ambiguity.'),
table(['Stone i', 'Height', 'From i − 1', 'From i − 2', 'best[i]'], K.frog_fill([10, 30, 20, 40]), r'>{\raggedright\arraybackslash}p{11mm}>{\raggedright\arraybackslash}p{11mm}XX>{\raggedright\arraybackslash}p{12mm}'),
'''For 100,000 equal heights every permitted jump costs 0 and the result is 0. The loop handles this without 100,000 nested calls. The supplied large test also has varied heights, so a function that always returns 0 cannot pass it.'''),
section('Frog: edge cases, mistakes and the judge', [], 'Prepare students to test Frog properly and to submit it to AtCoder.', 'Compare the two problems of this lesson.',
edges([['Two stones', 'their height difference', 'Only one jump exists; there is no stone i − 2 to read.'],
       ['Two equal stones [8, 8]', str(P.frog_table([8, 8])), 'A zero-cost jump is legal.'],
       ['[10, 20, 30]', str(P.frog_table([10, 20, 30])), 'Two different routes tie; the answer is still one number.'],
       ['100,000 equal heights', str(P.frog_table([7] * 100000)), 'Size: needs a loop, not recursion.'],
       ['Largest possible answer', 'at most ' + C(99999 * 9999), 'At most 99,999 jumps of at most 9,999: no overflow worry, even in other languages.']]),
mistakes([['take the cheaper next jump (greedy)', 'follows 0-2-3-5', f'{GREEDY_COST} ({BEST_COST})'],
          ['compare only the two jump costs', 'forgets the cost of reaching the earlier stone', K.run_variant('def frog(h):\n    best = [0] * len(h)\n    for i in range(1, len(h)):\n        one = abs(h[i] - h[i - 1])\n        two = abs(h[i] - h[i - 2]) if i >= 2 else one\n        best[i] = best[i - 1] + min(one, two)\n    return best[-1]\n', 'frog([20, 50, 30, 40, 10, 10])') + f' ({BEST_COST})'],
          ['`return sum(best)`', 'adds every stone\'s total cost', K.variant('frog_table', 'return best[-1]', 'return sum(best)', 'frog_table([20, 50, 30, 40, 10, 10])') + f' ({BEST_COST})'],
          ['no `i >= 2` check', 'stone 1 reads best[−1] and heights[−1]', K.variant('frog_table', 'if i >= 2:', 'if True:', 'frog_table([10, 30])') + ' on [10, 30] (20)'],
          ['frog_slow on 100,000 stones', 'the first call chain is 100,000 deep', K.variant('frog_slow', 'return cost(len(heights) - 1)', 'return cost(len(heights) - 1)', 'frog_slow([7] * 100000)')]]),
'''To submit, use the program below, which is exactly the file programs/frog_table.py: the function from this chapter followed by three lines that read the judge's input and print the answer.''',
judge('frog_table'),
python(['input', 'map', 'split'], 'reading the judge input', '''`input()` reads one line of standard input as text, and `int(…)` turns it into a number. `input().split()` cuts the second line into its words; `map(int, …)` converts each word to an integer and `list(…)` collects them, so `heights` is a list of numbers. `print` writes the answer to standard output.'''),
f'''Judge notes. AtCoder reads standard input and compares standard output, so the program must print only the number. Choose Python (CPython 3) or PyPy; either is fast enough here, since the loop runs 100,000 times (about {T_FROG*1000:.0f} ms on a laptop; the limit is 2 seconds). Do not submit a recursive version: it stops with a RecursionError on the long tests. The judge numbers stones from 1, but the input is just the list of heights, so nothing needs converting.''',
recap('best[i] (or cost(i)) is the cheapest total cost from stone 0 to stone i.',
      'Two candidates: from i − 1 and from i − 2, each its own total plus one jump; keep the minimum.',
      'Greedy fails on [20, 50, 30, 40, 10, 10]: 50 instead of 30.',
      'The loop fills left to right in O(n) time; the answer is best[-1].')),
section('What changed between the two problems?', ['L1-20'], 'Name what is the same and what differs in the two solutions, and restate the main idea.', 'Use the practice files to test both programs.',
table(['', 'Staircase', 'Frog'], [['Question for index i', 'number of routes to step i', 'cheapest cost to stone i'],
                                 ['Starting value', 'ways[0] = 1 (the empty route)', 'best[0] = 0 (no jump)'],
                                 ['Last moves', 'from i − 1 or i − 2', 'from i − 1 or i − 2'],
                                 ['Combine with', '+ (the groups are disjoint)', 'min (the totals compete)'],
                                 ['Order', 'increasing i', 'increasing i'],
                                 ['Answer', 'ways[n]', 'best[-1]']], r'>{\raggedright\arraybackslash}p{30mm}XX'),
'''Both problems organise the work by the final move. Staircase counts every valid route, so the disjoint last-move groups are added. Frog wants one cheapest total, so the candidate costs compete through `min`. The operation follows the meaning of the answer.

That is the main idea of the lesson: remember the answer. Dynamic programming means identifying repeated questions, storing their answers and evaluating them in an order where every needed answer is ready. It is not a rule saying to add previous list entries. A student who can say what an index identifies, what its stored value means, which earlier answers it needs and why the starting value is right has understood the lesson.'''),
)

appendix = [chapter('Summary tables', 'Reference tables for planning and for checking a student\'s claim quickly.',
section('Every algorithm in this lesson', [], 'Compare the cost of every program in one place.', 'Keep this page beside you while teaching.',
table(['Program', 'Time', 'Extra memory', 'Recursion depth', 'Use for'],
      [['stairs_slow', 'about 1.6ⁿ calls', 'O(n) stack', 'n + 1', 'tracing tiny cases'],
       ['stairs_cached', 'O(n): 2n + 1 calls', 'O(n)', 'n + 2', 'showing the cache'],
       ['stairs_table', 'O(n)', 'O(n)', 'none', 'the real solution'],
       ['stairs_13', 'O(n)', 'O(n)', 'none', 'the variation'],
       ['frog_slow', 'F(n + 2) − 1 calls', 'O(n) stack', 'n', 'tracing tiny cases'],
       ['frog_cached', 'O(n): 2n − 2 calls', 'O(n)', 'n', 'showing the cache'],
       ['frog_table', 'O(n)', 'O(n)', 'none', 'the judge'], ['frog_path', 'O(n)', 'O(n)', 'none', 'optional route recovery']], r'>{\raggedright\arraybackslash}p{24mm}XX>{\raggedright\arraybackslash}p{20mm}X'),
'''Here n is the target step or the number of stones. O(n) means "at most a constant times n operations". The Python features explained in this book are def and return, recursion, nested functions, dictionaries, import, try and except, list repetition, range, +=, negative indices, tuples, list comprehensions, abs, min and len.'''),
section('Planning the two hours', [], 'See the lesson plan and what may move to the next meeting.', 'This is the end of the book; the teacher guide follows the same plan.',
table(['Minutes', 'Activity', 'Questions'], [[a, b, ('L1-' + c.replace('-', ' to L1-')) if c else ''] for a, b, c in __import__('content').LESSONS[0]['plan']], r'>{\raggedright\arraybackslash}p{16mm}X>{\raggedright\arraybackslash}p{26mm}'),
'''Keep the full staircase and Frog progression in this lesson. Use the first eight minutes as a recursion refresher: trace one call and ask how it stops. L1-01 to L1-04 remain available for students who need more practice; do not require everyone to finish all four before starting the staircase. Aim to finish staircase by minute 60, take a five-minute break, and spend minutes 65 to 110 on Frog: whole-route costs, why greedy fails, exhaustive recursion, caching, then iteration and testing. Reserve the final ten minutes to compare what the two tables store. If students need longer on a coding task, give the partial code on the board and finish it together; keep both problem-solving progressions in the session.'''))]

BOOK = dict(
    idea='Remember the answer to each question so that it is never worked out twice, and then choose an order in which every answer you need is already known.',
    intro='We first trace functions that call themselves, learn how they stop, and write a small recursive function. Then we count routes up a staircase. The first program follows every choice, so we can see why its answer is correct. We then notice that many calls ask the same question. Saving their answers removes repeated work; filling a table in order also removes the deep call stack. Frog uses the same sequence of ideas, but its stored answers are costs rather than counts, so one problem adds answers and the other takes a minimum.',
    outcomes=['state each problem exactly and solve small cases by hand;',
              'explain a recurrence from the last move, including its starting values;',
              'count the calls of a slow recursion and point to the line that causes them;',
              'cache answers in a dictionary and explain why the call stack is still deep;',
              'fill a table with a loop, give its cost line by line, and submit Frog to AtCoder.'],
    front=['Read this book before the lesson. The separate teacher guide holds the short classroom prompts and answers; the margin notes here name the matching question IDs on the worksheet, slides and notebook. Every program is printed in full, and every number about running code (call counts, line counts, wrong outputs) was produced by running the programs.',
           'Students need Python functions, lists, loops, indexing, comparisons and basic arithmetic. Each new Python feature is explained in a grey PYTHON note beside the first program that uses it.',
           'Each section opens with its objective and ends by pointing to the next. Each problem ends with its edge cases, common mistakes (with the wrong output each one produces), how to submit it and a recap. The summary tables and the two-hour plan are in the appendix.'],
    chapters=[INTRO, ch1, ch2, ch3], appendix=appendix)
