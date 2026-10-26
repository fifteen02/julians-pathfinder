"""The recursion refresher gives students a task before revealing its trace."""
from pathlib import Path
import json, re, io, contextlib
import programs as P
import recursion_intro as RI
from sheet_guidance import IMPLEMENT
assert not set(RI.PROVIDED_TRACE_FUNCTIONS) & {fn for functions, _ in IMPLEMENT.values() for fn in functions}

ROOT = Path(__file__).resolve().parent.parent
nb = json.loads((ROOT / 'Lesson 1/lesson.ipynb').read_text())
cells = nb['cells']
text = '\n'.join(''.join(c['source']) for c in cells)
assert text.count('<details>') == 3
assert '<details open' not in text
for c in cells:
    assert not c.get('outputs'), 'Student notebook must not ship executed answers'
visible = re.sub(r'<details>.*?</details>', '', text, flags=re.S)
for row in RI.TRACE_ROWS[:-1]:
    assert row[2] not in visible, ('completed introductory trace exposed', row)
assert text.index('Your prediction and additions') < text.index('prediction = None') < text.index('<details>')
# Default Run All does not print the trace results; an explicit choice does.
intro_check = next(c['source'] for c in cells if c['cell_type']=='code' and 'prediction = None' in c['source'])
for source, names, expected in [
    (intro_check, {'sum_to':P.sum_to}, 'Returned value: 6'),
    (RI.trace_check('countdown',3), {'countdown':P.countdown}, '3\n2\n1\nGo!'),
    (RI.trace_check('sum_squares',4), {'sum_squares':P.sum_squares}, '30'),
]:
    output=io.StringIO()
    with contextlib.redirect_stdout(output): exec(source,names.copy())
    assert expected not in output.getvalue(), 'answer exposed on default execution'
    output=io.StringIO()
    opted_in=source.replace('prediction = None','prediction = 6').replace('run_example = False','run_example = True')
    with contextlib.redirect_stdout(output): exec(opted_in,names.copy())
    assert expected in output.getvalue(), (expected,output.getvalue())
# The source itself must put a question slide immediately before its worked answer.
slides=(ROOT/'Lesson 1/slides.tex').read_text().split(r'\begin{frame}')
q=next(i for i,s in enumerate(slides) if 'Trace sum\\_to(3): your turn' in s)
assert 'Trace sum\\_to(3): worked answer' in slides[q+1]
for row in RI.TRACE_ROWS[:-1]:
    assert row[2] not in slides[q]
    assert row[2] in slides[q+1]
# Do not pre-solve countdown(3) while introducing the idea of recursion.
first=next(s for s in slides if 'A function that calls itself' in s and '/ RECURSION' in s)
assert r'3\\2\\1\\Go!' not in first
print('PASS: separate question/answer slides; three closed notebook trace panels; predictions required before results; opted-in examples produce the correct output.')
