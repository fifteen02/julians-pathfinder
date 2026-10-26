"""Lesson 1 recursion warm-up: five teaching slides before L1-01, the matching
teacher-guide page and the notebook introduction. Questions L1-01 to L1-04
(content.py) practise each idea; no term is used before these slides teach it."""
import inspect
from html import escape
import programs as P

# These functions are supplied for tracing, not assigned for implementation.
PROVIDED_TRACE_FUNCTIONS = ('sum_to', 'countdown', 'sum_squares')

# The step table shown on the last teaching slide (worked example, sum_to(3)).
TRACE_HEAD = ['Call', 'Waits for', 'Returns']
TRACE_ROWS = [[f'sum_to({n})', f'sum_to({n-1})', f'{n} + {P.sum_to(n-1)} = {P.sum_to(n)}'] for n in (3,2,1)] + [['sum_to(0)', 'nothing (base case)', str(P.sum_to(0))]]

TRACE_QUESTION_ROWS = [[row[0], row[1], '?' if i < 3 else row[2]] for i, row in enumerate(TRACE_ROWS)]


def return_rows(fn, n, operation):
    """Arithmetic shown in exercise answers, evaluated using the reference code."""
    f = getattr(P, fn)
    rows = []
    for k in range(n, 0, -1):
        left = k * k if fn == 'sum_squares' else 2 if fn == 'power2' else k
        rows.append([f'{fn}({k})', f'{fn}({k-1})', f'{left} {operation} {f(k-1)} = {f(k)}'])
    return rows + [[f'{fn}(0)', 'nothing', str(f(0))]]


def _code_rows(fn, tex):
    rows = []
    for line in inspect.getsource(getattr(P, fn)).rstrip().splitlines():
        indent = len(line) - len(line.lstrip())
        colour='returnink' if line.strip() in ('return 0', 'return', "print('Go!')") else 'callink' if 'n - 1' in line else 'ink'
        rows.append((r'\hspace*{%.1fem}' % (indent * 0.6) if indent else '') + r'\textcolor{'+colour+'}{'+tex(line.strip())+'}')
    return r'\\'.join(rows)


def _code_node(fn, tex, at, size=22, name='code'):
    return (r'\node(' + name + r')[anchor=north west,inner sep=5mm,fill=codepaper,align=left,font=\ttfamily\fontsize{%d}{%d}\selectfont] at %s {'
            % (size, int(size * 1.25), at) + _code_rows(fn, tex) + '};\n')


def slides(start, end, stxt, number, ruled, tex):
    def head(title, objective, phase=""):
        return (start + '\n' + stxt(1.5, 16.9, 29, 13, r'\heavy LESSON 1 / RECURSION' + (' / ' + phase if phase else ''), 'returnink' if phase=='ANSWER' else 'callink') + number()
                + stxt(1.5, 15.4, 29, 34, r'\heavy ' + tex(title)) + stxt(1.5, 13.0, 29, 21, r'\textbf{Objective.} ' + tex(objective), 'quiet'))
    box = r'draw=callink,line width=1.4pt,rounded corners=3mm,minimum width=5.2cm,minimum height=1.6cm,font=\ttfamily\fontsize{20}{24}\selectfont'
    s = ''
    # 1. A function that calls itself.
    s += head('A function that calls itself', 'read a function that calls itself and follow what it prints.')
    s += _code_node('countdown', tex, '(1.5,11.2)')
    s += stxt(17.5, 11.2, 13, 22, r'Calling the same function from inside it is \textbf{recursion}. Each call has its own n. Here n is a nonnegative integer.' + r'\par\medskip In L1-01, trace countdown(3). Write its output before running it; the answer comes after your attempt.')
    s += stxt(1.5, 4.1, 14.5, 20, 'The argument gets smaller at every call, so the calls stop when n reaches 0.', 'teal') + end + '\n'
    # 2. Base case and smaller case.
    s += head('Two parts: a base case and a smaller case', 'name the two parts every recursive function needs.')
    s += stxt(1.5, 11.2, 14, 22, r'\textcolor{returnink}{\textbf{Base case:}} an input answered directly, with no further call. In countdown it is n == 0.')
    s += stxt(16.5, 11.2, 14, 22, r'\textcolor{callink}{\textbf{Smaller case:}} the function calls itself on a smaller input, which must lead to the base case.')
    s += r'\begin{scope}[>=Stealth]'
    s += r'\node(c0)[%s,fill=callwash] at (6,5.8) {countdown(n)};' % box
    s += r'\node(c1)[%s,fill=callwash] at (18,5.8) {countdown(n - 1)};' % box
    s += r'\draw[->,very thick,callink] (c0)--node[above,font=\fontsize{17}{20}\selectfont]{one smaller input}(c1);'
    s += r'\end{scope}' + '\n'
    s += stxt(1.5, 3.2, 29, 21, 'The smaller calls must eventually reach n == 0, where countdown makes no further call.') + end + '\n'
    # 3. The call stack.
    s += head('The call stack', 'see why a call waits, and where Python keeps waiting calls.')
    s += stxt(1.5, 11.5, 29, 19, tex('sum_to(n) returns 1 + 2 + ... + n; sum_to(0) returns 0. Data: n = 3.'))
    s += _code_node('sum_to', tex, '(1.5,10.0)')
    s += stxt(1.5, 5.0, 14.5, 20, r'\texttt{return} hands a value to the calling function. Python keeps unfinished calls on the \textbf{call stack}. The newest call is on top; the others wait for its answer.')
    for k, (label, note) in enumerate([('sum_to(3)', 'waits'), ('sum_to(2)', 'waits'), ('sum_to(1)', 'waits'), ('sum_to(0)', 'returns 0')]):
        y = 2.2 + k * 2.1
        fill = 'returnwash' if k == 3 else 'waitwash'
        s += r'\node(stack%d)[%s,draw=%s,fill=%s,minimum width=7cm] at (21.5,%.1f) {%s};' % (k, box, 'returnink' if k==3 else 'waitink', fill, y, tex(label))
        s += r'\node[anchor=west,font=\fontsize{18}{22}\selectfont,text=quiet] at (25.3,%.1f) {%s};' % (y, note) + '\n'
    s += r'\draw[-{Stealth[length=3mm]},callink,line width=2pt] (17.1,2.3)--node[left,rotate=90,anchor=south,font=\fontsize{16}{19}\selectfont]{new calls}(17.1,8.3);'
    s += r'\node[font=\fontsize{17}{20}\selectfont,text=returnink] at (21.5,9.8) {top: answer directly};' + end + '\n'
    # 4-5. Keep the trace task and its completed answer on separate slides.
    for answer in (False, True):
        s += head('Trace sum_to(3): ' + ('worked answer' if answer else 'your turn'),
                  'trace calls down the table, then work out returned values from the bottom up.',
                  'ANSWER' if answer else 'QUESTION')
        body = ('Read the completed Returns column from the bottom up. Each call adds its own n to the result it receives.'
                if answer else 'Data: n = 3. Fill the missing Returns entries, including each addition. Start with sum_to(0). Predict the final returned value before going to the next slide.')
        s += stxt(1.5, 11.2, 29, 21, tex(body), 'ink', 'body')
        rows = TRACE_ROWS if answer else TRACE_QUESTION_ROWS
        s += r'\node(trace)[anchor=north west,inner sep=0,text width=26cm] at (3,8.6) {' + ruled(TRACE_HEAD, rows, tex, True) + '};\n'
        s += r'\draw[-{Stealth[length=3mm]},callink,line width=2pt] (1.7,8)--node[left,rotate=90,anchor=south,font=\fontsize{16}{19}\selectfont]{calls go down}(1.7,4.3);'
        s += r'\draw[-{Stealth[length=3mm]},returnink,line width=2pt] (30.3,4.3)--node[right,rotate=90,anchor=north,font=\fontsize{16}{19}\selectfont]{answers come back}(30.3,8);'
        s += stxt(1.5, 2.4, 29, 20,
                  'Compare each addition with your prediction before continuing to L1-01.' if answer
                  else 'Pause here. The next slide contains the completed trace.', 'teal') + end + '\n'

    return s


def teacher(tex, ruled, code_listing):
    """A short teacher page for the five warm-up slides."""
    s = r'\labeltext{Recursion warm-up (before L1-01; slides 3 to 7)}' + '\n'
    s += tex('Objective: students read and write a function that calls itself, so that the staircase recursion is not their first recursive function. Teach in this order, using the slides: (1) a function may call itself on a smaller input (countdown); (2) the two parts: base case and smaller case; (3) a waiting call stays on the call stack until the smaller call returns; (4) show the incomplete sum_to(3) table and ask students to predict each returned value; (5) reveal the completed table on the following slide, after their attempt. Do not reveal the countdown output before L1-01. In the notebook, predictions come before the runnable checks and the closed answer panels. Allow eight minutes for this refresher. Use one of L1-01 to L1-04 to check understanding; keep the others as optional practice if students already know recursion. Continue to the staircase by minute 8 so that the full Frog progression fits after the break.') + '\n\n'
    s += r'\textbf{Worked example for the board.}' + code_listing(inspect.getsource(P.sum_to))
    s += ruled(TRACE_HEAD, TRACE_ROWS, tex) + r'\par\medskip' + '\n'
    return s


NOTEBOOK = """## Recursion refresher (before L1-01)

**Objective:** follow a function that calls itself and explain why it stops.

A function calling itself is **recursion**. It needs two parts:

- a **base case**: an input answered directly, with no further call;
- a **smaller case**: a call on a smaller input that leads to the base case.

**Code to trace.** The function below returns the sum of the integers from 1 to n. The base case sum_to(0) returns 0. Run the definition cell to make the function available; this does not call it or show the answer.
"""

STACK_NOTE = """`return` hands a value to the calling function. Python keeps unfinished calls on the **call stack**. Data: `n = 3`. Just before the base case returns, the stack looks like this:

```text
Top       sum_to(0)  can return 0 now
          sum_to(1)  waits for sum_to(0)
          sum_to(2)  waits for sum_to(1)
Bottom    sum_to(3)  waits for sum_to(2)
```

**Your turn.** Fill the missing Returns entries in the table, including each addition. Work from the bottom up. Then predict the value returned by `sum_to(3)`.
"""


def table_markdown(head, rows):
    return ' | '.join(head) + '\n' + ' | '.join(['---'] * len(head)) + '\n' + '\n'.join(' | '.join(row) for row in rows) + '\n'


def reveal_table(head, rows, label='Show the completed trace after your attempt'):
    # Raw HTML table inside native details avoids Markdown-in-HTML differences.
    header = '<tr>' + ''.join('<th>' + escape(cell) + '</th>' for cell in head) + '</tr>'
    body = ''.join('<tr>' + ''.join('<td>' + escape(cell) + '</td>' for cell in row) + '</tr>' for row in rows)
    return '<details><summary>' + escape(label) + '</summary>\n<table>' + header + body + '</table>\n</details>\n'


def notebook_cells(mdcell, codecell, teacher=False):
    cells = [mdcell(NOTEBOOK), codecell(inspect.getsource(P.sum_to)),
             mdcell(STACK_NOTE + '\n' + table_markdown(TRACE_HEAD, TRACE_QUESTION_ROWS)),
             mdcell('**Your prediction and additions:**\n\nWrite your working here before checking.')]
    cells.append(codecell("""# Replace None with your predicted result, then run this cell.
prediction = None
if prediction is None:
    print('Fill the trace and enter your prediction first.')
else:
    actual = sum_to(3)
    print('Your prediction:', prediction)
    print('Returned value:', actual)
    print('Compare each row of your trace with the worked answer below.')
"""))
    cells.append(mdcell('**Worked answer:**\n\n' + table_markdown(TRACE_HEAD, TRACE_ROWS) if teacher
                        else reveal_table(TRACE_HEAD, TRACE_ROWS)))
    return cells


def trace_check(fn, argument):
    return ("# Fill the table above before running this example.\n"
            "# Change False to True when you are ready to check.\n"
            "run_example = False\n"
            "if run_example:\n    "
            + (f"{fn}({argument})" if fn == 'countdown' else f"print({fn}({argument}))")
            + "\nelse:\n    print('Predict first. Set run_example to True to check your answer.')\n")
