"""Layout helpers for the classroom formats: ruled worksheet tables, drawing
spaces, numbered listings, printed calls and the code slides.

The tutor books do not use these helpers, so their pages are unaffected.
"""
import ast

# ---------------------------------------------------------------- listings
# Code listings in the teacher guide and the answer booklet are numbered in the
# same style as the tutor book. Inputs, outputs and traces stay unnumbered.
NUMBERED_STYLE = (r'\lstdefinestyle{numbered}{numbers=left,numberstyle=\ttfamily\fontsize{7.5}{13}\selectfont\color{lightink},'
                  r'numbersep=10pt,xleftmargin=24pt}')


def numbered(code):
    return '\n' + r'\begin{lstlisting}[style=numbered]' + '\n' + code.rstrip() + '\n' + r'\end{lstlisting}' + '\n'


# ---------------------------------------------------------------- calls
def call_args(args):
    """'([7] * 100000,)' -> '[7] * 100000'; "('HHSSP', 1)" -> "'HHSSP', 1"."""
    tree = ast.parse(args, mode='eval').body
    items = tree.elts if isinstance(tree, ast.Tuple) else [tree]
    return ', '.join(ast.get_source_segment(args, item) for item in items)


def call_text(fn, args):
    return f'{fn}({call_args(args)})'


# ---------------------------------------------------------------- tables
def ruled(head, rows, tex, slide=False):
    """One table style for worksheets and slides: every cell ruled, about 8 mm tall.
    '?' marks an unknown cell in the shared content and prints as an empty cell."""
    n = len(head)
    longest = max(len(str(r[0])) for r in [head] + rows)
    tall = False
    if slide:
        # Taller tables get shorter rows so they stay clear of the slide number.
        tall = len(rows) >= 4
        size = r'\fontsize{20}{24}\selectfont' if tall else r'\fontsize{22}{26}\selectfont'
        height, label = ('10mm' if len(rows) >= 5 else '11.5mm') if tall else '13.5mm', min(max(longest * 5.2, 34), 130)
    else:
        size, height, label = (r'\footnotesize' if n > 9 else r'\small'), '8mm', min(max(longest * 2.1, 18), 68)
    if slide == 'compact':
        size, height, tall = r'\fontsize{18}{22}\selectfont', '8.5mm', True
    depth = ('-3.4mm' if tall else '-4.6mm') if slide else '-2.7mm'
    head_strut = (r'\rule[-2.6mm]{0pt}{8mm}' if tall else r'\rule[-3mm]{0pt}{9.5mm}') if slide else r'\rule[-2mm]{0pt}{6.5mm}'
    cols = '|' + r'>{\raggedright\arraybackslash}p{' + f'{label:.0f}mm' + '}|' + (r'>{\centering\arraybackslash}X|' * (n - 1))

    def cell(x):
        return '' if str(x) == '?' else tex(x)
    strut = r'\rule[' + depth + ']{0pt}{' + height + '}'
    out = r'\begingroup' + size + r'\setlength{\tabcolsep}{5pt}\setlength{\arrayrulewidth}{.5pt}\arrayrulecolor{quiet}\renewcommand{\arraystretch}{1}'
    out += r'\begin{tabularx}{\linewidth}{' + cols + r'}\hline' + '\n'
    out += r'\rowcolor{wash}' + head_strut + ' & '.join(r'\textbf{' + tex(x) + '}' for x in head) + r'\\\hline' + '\n'
    for row in rows:
        out += strut + ' & '.join(cell(x) for x in row) + r'\\\hline' + '\n'
    return out + r'\end{tabularx}\endgroup'


# ---------------------------------------------------------------- code slides
# Slide geometry in points: the code panel sits below the title and above the
# slide number. JetBrains Mono advances 0.6 em per character.
CODE_HEIGHT = 316
CODE_WIDTH = 805
ONE_SLIDE = 17   # keep a function whole when it fits at this size or larger
MAX_SIZE, MIN_SIZE = 24, 15
LEADING = 1.12


def code_metrics(chunk, size, last_number):
    digits = len(str(last_number))
    number_size = round(size * 0.65, 1)
    left = 12 + digits * 0.6 * number_size + 2
    width = left + 0.6 * size * max(len(line) for line in chunk) + 6
    return width, len(chunk) * LEADING * size, left, number_size


def fit_size(chunks, total):
    for tenth in range(MAX_SIZE * 2, MIN_SIZE * 2 - 1, -1):
        size = tenth / 2
        if all(code_metrics(c, size, total)[0] <= CODE_WIDTH and code_metrics(c, size, total)[1] <= CODE_HEIGHT for c in chunks):
            return size
    return None


def boundaries(lines):
    """Indices where a new top-level statement of the function (or module) starts."""
    depth = 0
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        after_decorator = i and lines[i - 1].strip().startswith('@')
        if i and depth == 0 and stripped and indent <= 4 and not after_decorator and not stripped.startswith(('else', 'elif', 'except', 'finally', 'return')):
            result.append(i)
        depth += sum(line.count(c) for c in '([{') - sum(line.count(c) for c in ')]}')
    return result


def split_code(lines):
    """Whole function on one slide when it fits; otherwise split only where a
    top-level statement begins, choosing the most even split."""
    total = len(lines)
    whole = fit_size([lines], total)
    if whole and whole >= ONE_SLIDE:
        return [(0, lines)]
    cuts = boundaries(lines)
    best = None
    for parts in (2, 3):
        options = []
        if parts == 2:
            options = [(a,) for a in cuts]
        else:
            options = [(a, b) for a in cuts for b in cuts if b > a]
        for opt in options:
            edges = (0,) + opt + (total,)
            chunks = [lines[edges[k]:edges[k + 1]] for k in range(parts)]
            # No thin slides: every part keeps at least five lines of code.
            if min(sum(1 for x in c if x.strip()) for c in chunks) < 5:
                continue
            size = fit_size(chunks, total)
            if size:
                score = (max(len(c) for c in chunks), -size)
                if best is None or score < best[0]:
                    best = (score, [(edges[k], chunks[k]) for k in range(parts)])
        if best:
            break
    if whole and (not best or -best[0][1] < whole + 2):
        return [(0, lines)]
    assert best, 'code cannot be split at a statement boundary'
    out = []
    for start, chunk in best[1]:
        while chunk and not chunk[0].strip():
            start, chunk = start + 1, chunk[1:]
        while chunk and not chunk[-1].strip():
            chunk = chunk[:-1]
        out.append((start, chunk))
    return out


def code_slides(header, title, code, tex):
    """Code frames in the same layout as the question and answer slides."""
    lines = code.rstrip().splitlines()
    chunks = split_code(lines)
    size = fit_size([c for _, c in chunks], len(lines))
    out = ''
    for k, (start, chunk) in enumerate(chunks):
        width, _, left, number_size = code_metrics(chunk, size, len(lines))
        out += r'\begin{frame}[plain,fragile]' + '\n'
        out += r'\begin{lrbox}{\codebox}\begin{minipage}{' + f'{width:.0f}pt' + '}\n'
        out += (r'\begin{lstlisting}[basicstyle=\ttfamily\fontsize{' + f'{size}' + '}{' + f'{size * LEADING:.1f}' + r'}\selectfont\color{ink},'
                r'numbers=left,numberstyle=\ttfamily\fontsize{' + f'{number_size}' + '}{' + f'{size * LEADING:.1f}' + r'}\selectfont\color{quiet},'
                r'numbersep=12pt,xleftmargin=' + f'{left:.0f}pt' + r',firstnumber=' + str(start + 1) + r',breaklines=false,aboveskip=0pt,belowskip=0pt]' + '\n')
        out += '\n'.join(chunk) + '\n' + r'\end{lstlisting}' + '\n' + r'\end{minipage}\end{lrbox}' + '\n'
        out += r'\begin{tikzpicture}[remember picture,overlay,x=1cm,y=1cm]\begin{scope}[shift={(current page.south west)}]' + '\n'
        out += header
        part = f' ({k + 1} of {len(chunks)})' if len(chunks) > 1 else ''
        out += (r'\node[anchor=north west,inner sep=0pt,text width=29cm,align=left,text=ink,font=\fontsize{34}{40.8}\selectfont] at (1.5,15.4) {\heavy '
                + tex(title) + part + '};\n')
        out += r'\node[anchor=north,inner sep=5mm,fill=codepaper] at (16,13.6) {\usebox{\codebox}};' + '\n'
        if k < len(chunks) - 1:
            out += r'\node[anchor=south west,inner sep=0pt,text=quiet,font=\fontsize{16}{19}\selectfont] at (1.5,0.7) {The function continues on the next slide.};' + '\n'
        out += r'\end{scope}\end{tikzpicture}' + '\n' + r'\end{frame}' + '\n'
    return out
