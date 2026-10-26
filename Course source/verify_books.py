"""Checks for the five tutor books (build/Lesson N/tutorial.tex and build/Lesson N/tutorial.pdf).

1. Every count the books print about running code is re-derived independently
   (closed forms, brute force) and must appear in the generated .tex.
2. Every section states an objective and points to the next; every problem
   statement comes before the first listing of its chapter.
3. Every Python feature in the curated list is explained in a PYTHON note beside
   the first listing (or test line) that uses it, in each book separately.
4. The judge programs printed in the books equal the files in Lesson N/programs/.
5. The compiled PDFs: no listing split across pages, no Computer Modern fonts,
   the lesson's main idea on page 2.
Run after build_course.py and compile_all.py.
"""
from pathlib import Path
import ast, re, subprocess, sys
sys.dont_write_bytecode = True
import programs as P
import book_kit as K
import build_course as B
from book_content import BOOKS
from content import LESSONS
from compile_all import build_dir
ROOT = Path(__file__).resolve().parent.parent
checks = 0


def check(cond, label):
    global checks
    assert cond, label
    checks += 1


# 1. Counts, against closed forms and brute force -------------------------------
fib = K.fib
for n in range(0, 31):
    check(K.calls(P.stairs_slow, (n,)) == 2 * fib(n + 2) - 1, ('stairs_slow calls', n))
    check(K.calls(P.stairs_cached, (n,), 'ways') == 2 * n + 1, ('stairs_cached calls', n))
check(K.calls(P.stairs_slow, (30,)) == 4_356_617, 'stairs_slow(30) = 4,356,617 calls')
for s in range(2, 31):
    h = list(range(s))
    check(K.calls(P.frog_slow, (h,), 'cost') == fib(s + 2) - 1, ('frog_slow calls', s))
    check(K.calls(P.frog_cached, (h,), 'cost') == 2 * s - 2, ('frog_cached calls', s))
check(K.calls(P.frog_slow, (list(range(30)),), 'cost') == 2_178_308, 'frog_slow 30 stones')
for n in range(0, 21):
    def dice_calls(t):
        return 1 + sum(dice_calls(t - f) for f in range(1, min(6, t) + 1))
    check(K.calls(P.dice_slow, (n,)) == dice_calls(n), ('dice_slow calls', n))
    check(K.calls(P.dice_cached, (n,), 'count') == 1 + sum(min(6, t) for t in range(1, n + 1)), ('dice_cached calls', n))
    if n <= 6:
        check(K.calls(P.dice_slow, (n,)) == 2 ** n, ('dice_slow 2^n', n))
for n in range(1, 8):
    check(len(K.stairs_routes(n)) == P.stairs_table(n), ('routes', n))
    check(len(K.dice_sequences(n)) == P.dice_table(n), ('sequences', n))
check(len(K.grid_routes(['....', '..*.', '*...', '....'])) == 7, 'grid example routes')

expected = {1: ['4,356,617', '2,178,308', '35,421', '17,710', '2,090-digit', '0-2-4-5', '0-2-3-5'],
            2: ['935,680', '5,999,985', '874,273,980', '965,601,742'],
            3: ['999,990,100', '9,999,901', '66,667', '879,725,732'],
            4: ['4,969,282', '5,000,002'],
            5: ['17,999,820', '6,299,937', '100,000']}
for n, numbers in expected.items():
    tex = (__import__('compile_all').source_path(n, 'tutorial')).read_text()
    for x in numbers:
        check(x in tex, (n, 'number missing from tutorial', x))

# 2. Structure ----------------------------------------------------------------
for n, book in BOOKS.items():
    for ch in book['chapters'] + book.get('appendix', []):
        for sec in ch['sections']:
            check(bool(sec['goal']), (n, sec['title'], 'objective'))
            check(bool(sec['next']), (n, sec['title'], 'next pointer'))
        blocks = [b for sec in ch['sections'] for b in sec['blocks']]
        kinds = [b[0] for b in blocks if isinstance(b, tuple)]
        if 'code' in kinds and 'problem' in kinds:
            check(kinds.index('problem') < kinds.index('code'), (n, ch['title'], 'problem stated before code'))
    check(book['chapters'][0]['sections'][0]['blocks'][1][0] == 'problem', (n, 'first section states the problem'))

# 3. Python features beside their first listing ---------------------------------
def features(source):
    found = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.decorator_list: found.add('decorator')
            if any(isinstance(c, ast.FunctionDef) for c in ast.walk(node) if c is not node): found.add('nested')
        if isinstance(node, ast.Dict): found.add('dict')
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod): found.add('mod')
        if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Mod): found.add('modassign')
        if isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, ast.FloorDiv): found.add('floordiv')
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name in ('enumerate', 'bytearray', 'abs', 'min', 'max', 'sum'): found.add(name)
            if name == 'range' and len(node.args) == 3: found.add('negstep')
            if name == 'int' and node.args and isinstance(node.args[0], (ast.Compare, ast.BoolOp)): found.add('int-bool')
            if name == 'float' and node.args and getattr(node.args[0], 'value', None) == 'inf': found.add('inf')
        if isinstance(node, ast.Slice): found.add('slice')
        if isinstance(node, ast.ListComp): found.add('listcomp')
        if isinstance(node, ast.GeneratorExp): found.add('genexp')
        if isinstance(node, ast.Continue): found.add('continue')
        if isinstance(node, ast.Try): found.add('try')
        if isinstance(node, ast.IfExp): found.add('ifexpr')
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and isinstance(node.left, ast.List): found.add('listmul')
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.UnaryOp) and isinstance(node.slice.op, ast.USub): found.add('negindex')
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('input', 'map', 'open'): found.add(node.func.id)
        if isinstance(node, ast.With): found.add('with')
        if isinstance(node, ast.Attribute) and node.attr in ('split', 'strip', 'read', 'write'): found.add(node.attr)
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Constant) and isinstance(node.iter.value, str): found.add('strloop')
    return found


for n, book in BOOKS.items():
    explained, pending = set(), []
    def settle():
        for name, needs in pending:
            missing = needs - explained
            check(not missing, (n, name, 'Python feature not explained beside its first listing', sorted(missing)))
        pending.clear()
    for ch in book['chapters']:
        for sec in ch['sections']:
            for b in sec['blocks']:
                if isinstance(b, tuple) and b[0] == 'code':
                    settle()
                    src = B.precode(b[1]) + '\n' + (b[2] or '')
                    new = features(src) - explained
                    pending.append((b[1], new))
                elif isinstance(b, tuple) and b[0] == 'judge':
                    settle()
                    pending.append(('programs/' + b[1], features(B.precode(b[1]) + '\n' + B.WRAPPERS[b[1]]) - explained))
                elif isinstance(b, tuple) and b[0] == 'python':
                    explained |= set(b[1])
            settle()

# 4. Judge programs --------------------------------------------------------------
for n, fns in B.FUNCTIONS.items():
    tex = (__import__('compile_all').source_path(n, 'tutorial')).read_text()
    for fn in fns:
        text = (ROOT / f'Lesson {n}/programs/{fn}.py').read_text()
        check(text == B.precode(fn) + '\n' + B.WRAPPERS[fn], (n, fn, 'programs file'))
        check(text.rstrip() in tex, (n, fn, 'judge program printed verbatim'))

# 5. PDFs -----------------------------------------------------------------------
for L in LESSONS:
    pdf = build_dir(L['n']) / 'tutorial.pdf'
    text = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True).stdout
    check('(continued)' not in text, (L['n'], 'listing split across pages'))
    fonts = subprocess.run(['pdffonts', str(pdf)], capture_output=True, text=True).stdout
    # Drop the random six-letter subset tags (e.g. LMXTQP+AvenirNext), which can look like LM fonts.
    fonts = re.sub(r'\b[A-Z]{6}\+', '', fonts)
    check(not re.search(r'\b(CM[A-Z]+\d+|LM[A-Za-z]+)', fonts), (L['n'], 'Computer Modern font in the PDF'))
    page2 = subprocess.run(['pdftotext', '-f', '2', '-l', '2', str(pdf), '-'], capture_output=True, text=True).stdout
    check(L['title'] in page2 and 'MAIN IDEA' in page2, (L['n'], 'main idea on page 2'))

report = f'PASS: {checks} tutor-book checks (counts re-derived, structure, Python notes, judge programs, PDF layout).'
(Path(__file__).with_name('book-verification.txt')).write_text(report + '\n')
print(report)
