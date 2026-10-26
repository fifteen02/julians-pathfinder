"""The short recursion chapter that precedes the Lesson 1 staircase."""
import contextlib
import io
import programs as P
from recursion_intro import TRACE_HEAD, TRACE_ROWS, return_rows
from book_blocks import chapter, section, problem, code, python, table, figure, listing, cost, recap

printed = io.StringIO()
with contextlib.redirect_stdout(printed):
    P.countdown(3)
COUNTDOWN_ROWS = [[f'countdown({n})', value, f'countdown({n-1})' if n else 'no new call']
                  for n, value in zip(range(3,-1,-1), printed.getvalue().splitlines())]
STACK = r'''\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth]
\node[anchor=west,font=\small] at (-2.5,3.1) {Newest call: answers first};
\node[draw,fill=wash,minimum width=4.7cm,minimum height=.7cm] at (0,2.4) {sum\_to(0): returns 0};
\node[draw,minimum width=4.7cm,minimum height=.7cm] at (0,1.5) {sum\_to(1): waits};
\node[draw,minimum width=4.7cm,minimum height=.7cm] at (0,.6) {sum\_to(2): waits};
\node[draw,minimum width=4.7cm,minimum height=.7cm] at (0,-.3) {sum\_to(3): waits};
\draw[->,thick] (2.8,2.4)--node[right,font=\small,align=left]{Values return\\to waiting calls}(2.8,-.3);
\end{tikzpicture}'''

INTRO = chapter('Recursion: follow one smaller call',
    'Read a function that calls itself, see how it stops, then write one before trying staircase.',
    section('A function can call itself', ['L1-01'],
        'Follow each call and distinguish printing a line from returning a value.',
        'Use a stopping case to end the chain of calls.',
        'We begin with a countdown. The input is the nonnegative integer n. For the worked example, n is 3. A new call receives its own value of n; it does not change the input held by the call that made it.',
        problem(name='Countdown', story='Print a countdown before starting an activity.',
            rules='Print each integer from n down to 1, one per line, then print Go! once. For n = 0, print only Go!.',
            input='a nonnegative integer n, supplied as a function argument.', output='the printed countdown.',
            limits='use n from 0 to 5 for these hand traces.', example_in='countdown(3)',
            example_out='3, then 2, then 1, then Go! (separate lines)',
            why='The table below follows the actual print order.', source='original teaching exercise.'),
        'A function calling itself is called recursion. In the listing, countdown(n - 1) makes a new call with an input one smaller. The current call pauses until that call has finished.',
        code('countdown'),
        python(['def','recursion'], 'print and return',
            '`def countdown(n):` names the function and its input. `print` writes a line on screen; it does not finish the function. `return` finishes the current call immediately. Here the bare `return` gives no numerical answer. The indented lines under `if n == 0:` run only for that input.'),
        table(['Call', 'Prints', 'Next call'], COUNTDOWN_ROWS),
        'The base case is the input answered without another recursive call. Here it is n = 0. Every other call reduces a positive n by 1, so it eventually reaches that base case. L1-01 asks students to reconstruct this trace.'),
    section('A call waits for a returned value', ['L1-02'],
        'Follow the waiting calls and calculate their answers from the base case upward.',
        'Repair a function whose calls never reach a stopping case.',
        'Now sum_to(n) returns the sum of the integers from 1 through n. For n = 0 it returns 0. Our example is sum_to(3). Unlike countdown, this function returns a number; it does not print the intermediate numbers.',
        code('sum_to'),
        'The expression n + sum_to(n - 1) cannot finish its addition until the smaller call returns. Python keeps unfinished calls on the call stack: the newest call is on top, with the calls waiting for it underneath.',
        figure(STACK, 'The stack after sum_to(3) has called down to sum_to(0). The top call can answer directly; the other three are waiting.'),
        'Calls enter the table from top to bottom. Evaluate the Returns column from bottom to top, using the result of the row below.',
        table(TRACE_HEAD, TRACE_ROWS),
        'For L1-02, sum_squares(n) returns the sum of the squares from 1 through n. The data is n = 4. Each waiting call adds n * n, rather than n.',
        code('sum_squares'), table(TRACE_HEAD, return_rows('sum_squares',4,'+'))),
    section('Find and repair the missing base case', ['L1-03'],
        'Identify why calls continue past the intended stopping input.',
        'Write a recursive function from a stated rule.',
        'power2(n) should return 2 raised to the nonnegative integer n. For example, the data n = 3 means multiplying three copies of 2. The worksheet supplies this deliberately incomplete function. Trace it on paper before running it.',
        listing('def power2(n):\n    return 2 * power2(n - 1)'),
        table(['Call number', 'Input n', 'Next input'], [[str(i+1),str(n),str(n-1)] for i,n in enumerate(range(3,-2,-1))]),
        'No call answers directly, so the input passes 0 and keeps decreasing. Python eventually raises RecursionError when too many calls are unfinished. The exact failing depth varies. The repair needs a stopping case before the recursive call. By definition, 2 raised to 0 is 1.',
        code('power2'), table(TRACE_HEAD,return_rows('power2',3,'x'))),
    section('Write one small recursive function', ['L1-04'],
        'Write factorial using a directly known answer and one smaller call.',
        'Try the staircase, where one call will ask two smaller questions.',
        'The factorial of n is the product of the integers from 1 through n; factorial(0) is defined as 1. Use nonnegative integers. Ask students to write the function before showing this solution. The worked example uses n = 4.',
        code('factorial'), table(TRACE_HEAD,return_rows('factorial',4,'x')),
        cost('Which lines do the work?', 'factorial', ((4,), {'n':4}, 'n = 4'), ({'n':10}, 'n = 10'),
            [('if n == 0:', 'once for every call, including the base case', lambda n:n+1),
             ('return n * factorial(n - 1)', 'once for each positive input', lambda n:n)]),
        'There is one smaller call for each positive input. The number of calls and the maximum number of unfinished calls both grow in proportion to n; this is O(n) call work and O(n) stack space. Multiplying large integers takes more work than multiplying small ones, so this counts calls rather than every arithmetic operation.',
        recap('A base case answers without another call.', 'Every recursive call must move toward a base case.',
              'A returned value goes back to the waiting call.', 'The staircase will ask two smaller questions instead of one.')))
