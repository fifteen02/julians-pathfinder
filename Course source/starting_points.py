"""Starting points for implementation questions: the exact signatures from
solutions.py (nested functions included) and short hints, rendered for the
worksheet, slides, teacher guide and notebook stubs. Data: sheet_guidance.IMPLEMENT."""
import inspect
import ast
import textwrap
import programs as P
from sheet_guidance import IMPLEMENT


# These are output meanings, not recurrences or completed helper bodies.
RETURNS = {
 'power2': [('power2(n)', 'the integer 2 raised to the power n.')],
 'factorial': [('factorial(n)', 'the product of integers 1 through n; for n = 0, return 1.')],
 'stairs_slow': [('stairs_slow(n)', 'the number of ordered routes to step n using jumps of 1 or 2.')],
 'stairs_table': [('stairs_table(n)', 'the number of ordered routes to step n using jumps of 1 or 2.')],
 'stairs_13': [('stairs_13(n)', 'the number of ordered routes to step n using jumps of 1 or 3.')],
 'frog_slow': [('frog_slow(heights)', 'the cheapest total cost from stone 0 to the last stone.'), ('cost(i)', 'the cheapest total cost from stone 0 to stone i, including all jumps along the route.')],
 'frog_table': [('frog_table(heights)', 'the cheapest total cost from stone 0 to the last stone.')],
 'frog_path': [('frog_path(heights)', 'a pair (cost, path): the minimum total cost and a list of stone indices from 0 to the last stone. On equal candidate costs, keep the predecessor i - 1.')],
 'dice_slow': [('dice_slow(n)', 'the exact number of ordered dice sequences with total n.')],
 'dice_cached': [('dice_cached(n)', 'the count for total n, modulo 1,000,000,007.'), ('count(total)', 'the count for this total, modulo 1,000,000,007.')],
 'dice_table': [('dice_table(n)', 'the number of ordered dice sequences with total n, modulo 1,000,000,007.')],
 'dice_123': [('dice_123(n)', 'the number of ordered sequences of 1, 2 and 3 with total n, modulo 1,000,000,007.')],
 'grid_cached': [('grid_cached(rows)', 'the number of legal paths from top-left to bottom-right, modulo 1,000,000,007.'), ('count(r, c)', 'the number of legal paths from top-left to cell (r, c), modulo 1,000,000,007.')],
 'grid_table': [('grid_table(rows)', 'the number of legal paths from top-left to bottom-right, modulo 1,000,000,007.')],
 'tower_cached': [('tower_cached(bosses)', 'the minimum total points paid by your friend, who starts.'), ('cost(i, friend_turn)', 'the minimum further points your friend must pay from boss i, with the indicated player next.')],
 'tower_table': [('tower_table(bosses)', 'the minimum total points paid by your friend, who starts.')],
 'array_cached': [('array_cached(values, m)', 'the number of valid completed arrays, modulo 1,000,000,007.'), ('count(i, previous)', 'the number of valid completions from position i with the given previous value, modulo 1,000,000,007.')],
 'array_rolling': [('array_rolling(values, m)', 'the number of valid completed arrays, modulo 1,000,000,007.')],
 'feast_cached': [('feast_cached(limit, a, b)', 'the greatest reachable fullness, starting empty with water unused.'), ('best(fullness, used_water)', 'the greatest final fullness reachable from this fullness and water status.')],
 'feast_table': [('feast_table(limit, a, b)', 'the greatest reachable fullness, starting empty with water unused.')],
 'hps_cached': [('hps_cached(john, budget)', 'the most rounds Bessie can win within the switch budget.'), ('best(i, left, previous)', 'the most further wins from round i, with left switches available and previous as the last gesture.')],
 'hps_table': [('hps_table(john, budget)', 'the most rounds Bessie can win within the switch budget.')],
}


def contracts(ident):
    return [pair for fn in IMPLEMENT[ident][0] for pair in RETURNS[fn]]


def outer_wiring(fn):
    """The supplied final helper call, plus assignments its arguments need."""
    source = inspect.getsource(getattr(P, fn))
    tree = ast.parse(source).body[0]
    helpers = [x for x in tree.body if isinstance(x, ast.FunctionDef)]
    if not helpers:
        return [], None
    final = tree.body[-1]
    assert isinstance(final, ast.Return) and isinstance(final.value, ast.Call)
    names = {x.id for x in ast.walk(final.value) if isinstance(x, ast.Name)}
    setup = [ast.get_source_segment(source, x) for x in tree.body
             if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in x.targets)]
    return setup, ast.get_source_segment(source, final)


def scaffold_lines(fn):
    definitions = signature_lines(fn)
    setup, final = outer_wiring(fn)
    out = [definitions[0]] + ['    ' + line for line in setup]
    if final:
        for definition in definitions[1:]:
            out += [definition, '        return None  # Your helper goes here.']
        out += ['    ' + final]
    else:
        out += ['    return None  # Replace with your answer.']
    return out


def signature_lines(fn):
    """Only the exact def lines; caching decorators are taught with the solution."""
    src = inspect.getsource(getattr(P, fn)).splitlines()
    out = []
    for i, line in enumerate(src):
        s = line.strip()
        if s.startswith('def '):
            out.append(line)
    return out


def start_lines(ident):
    """All signature lines for a question, one function after another."""
    fns, _ = IMPLEMENT[ident]
    lines = []
    for k, fn in enumerate(fns):
        if k:
            lines.append('')
        lines += scaffold_lines(fn)
    return lines


def hints(ident):
    return IMPLEMENT[ident][1]


def code_tex(lines, tex, size=r'\small'):
    """Monospaced lines on code paper, without a verbatim environment."""
    rows = []
    for line in lines:
        indent = len(line) - len(line.lstrip())
        rows.append((r'\hspace*{%.1fem}' % (indent * 0.6) if indent else '') + tex(line.strip()) if line.strip() else r'\mbox{}')
    return (r'\par\smallskip\noindent\colorbox{codepaper}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{' + size
            + r'\ttfamily\raggedright ' + r'\\'.join(rows) + '}}\\par\n')


def print_tex(ident, tex, label_start='Start with:', label_hints='Hints.'):
    """Starting code, output meanings and hints for printed classroom material."""
    s = r'\par\smallskip{\small\textbf{' + label_start + '}}' + code_tex(start_lines(ident), tex)
    s += r'{\small\textbf{What each function returns.}\par ' + ''.join(tex(call) + ': ' + tex(meaning) + r'\par ' for call, meaning in contracts(ident)) + '}\n'
    s += r'{\small\textbf{' + label_hints + r'}}\begin{itemize}' + ''.join(r'\item ' + tex(h) for h in hints(ident)) + r'\end{itemize}' + '\n'
    return s


def slide_nodes(ident, tex, anchor):
    """Code and return meanings side by side, with shared hints underneath."""
    rows = []
    for line in start_lines(ident):
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        line = line.split('  #')[0]
        if line.strip() == 'return None':
            line += '  # Replace this'
        rows.append((r'\hspace*{%.1fem}' % (indent * 0.6) if indent else '') + tex(line.strip()))
    s = (r'\node(sig)[anchor=north west,inner sep=3mm,fill=codepaper,align=left,font=\ttfamily\fontsize{16}{20}\selectfont] '
         r'at ([yshift=-4mm,xshift=3mm]' + anchor + r'.south west) {' + r'\\'.join(rows) + '};\n')
    details = r'\textbf{Returns}\par ' + ''.join(r'\textbf{' + tex(call) + '}: ' + tex(meaning) + r'\par\smallskip ' for call, meaning in contracts(ident))
    s += (r'\node(result)[anchor=north west,inner sep=0pt,text width=13.5cm,align=left,text=quiet,font=\fontsize{17}{20}\selectfont] '
          r'at ([yshift=-4mm,xshift=15.5cm]' + anchor + r'.south west) {' + details + '};\n')
    s += r'\node(both)[fit=(sig)(result),inner sep=0] {};' + '\n'
    s += (r'\node[anchor=north west,inner sep=0pt,text width=29cm,align=left,text=quiet,font=\fontsize{18}{22}\selectfont] '
          r'at ([yshift=-3mm,xshift=-3mm]both.south west) {\textbf{Hints.} ' + ' '.join(tex(h) for h in hints(ident)) + '};\n')
    return s


def stub(fn, doc):
    """Keep the outer helper call; students supply each helper's returned result."""
    definitions = signature_lines(fn)
    body = '\n'.join(textwrap.wrap(doc, 72, initial_indent='    ', subsequent_indent='    '))
    out = [definitions[0], '    """', body, '    """']
    setup, final = outer_wiring(fn)
    out += ['    ' + line for line in setup]
    for i, definition in enumerate(definitions[1:], 1):
        out.append(definition)
        pad = ' ' * (len(definition) - len(definition.lstrip()) + 4)
        out += [pad + '# Returns ' + RETURNS[fn][i][1], pad + '# Write this helper here.', pad + 'return None']
    out += ['    ' + final] if final else ['    # Replace this return with your solution.', '    return None']
    return '\n'.join(out) + '\n'


def markdown(ident):
    """The same starting code, output meanings and hints in the notebook."""
    return ('**Start with:**\n\n```python\n' + '\n'.join(start_lines(ident))
            + '\n```\n\n**What each function returns:**\n'
            + ''.join('- `' + call + '`: ' + meaning + '\n' for call, meaning in contracts(ident))
            + '\n**Hints:**\n' + ''.join('- ' + h + '\n' for h in hints(ident)))


def slide_code(code, tex, anchor):
    """Code printed with a question, as a panel below the named slide node."""
    rows = []
    for line in code.rstrip().splitlines():
        indent = len(line) - len(line.lstrip())
        rows.append((r'\hspace*{%.1fem}' % (indent * 0.6) if indent else '') + tex(line.strip()))
    return (r'\node(given)[anchor=north west,inner sep=3.5mm,fill=codepaper,align=left,font=\ttfamily\fontsize{16}{20}\selectfont] '
            r'at ([yshift=-7mm,xshift=3.5mm]' + anchor + r'.south west) {' + r'\\'.join(rows) + '};\n')
