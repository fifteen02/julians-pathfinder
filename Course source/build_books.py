"""Generate the five tutor books (build/Lesson N/tutorial.tex) from book_content.py.

Block types used in book_lN.py (see book_content.py for the constructors):
  str                         a paragraph (backticks give code font)
  ('code', name, run)         a complete listing from programs.py, optional run line
  ('table', head, rows, spec) a booktabs table; spec optionally sets column types
  ('diagram', unit_id)        a diagram shared with the classroom formats
  ('figure', tikz, caption)   a book figure from book_figures.py
  ('pause', question, answer) an AT THE BOARD box
  ('python', ids, title, text) a Python note beside the listing that first needs it
  ('problem', statement)      the full problem statement box
  ('cost', title, rows)       line | code | runs | totals, measured by book_kit
  ('items', [text, ...])      a bulleted list
  ('listing', text)           verbatim text such as an input file or a command
  ('judge', fn)               the exact judge program from Lesson N/programs/
"""
from pathlib import Path
from book_content import BOOKS
from content import LESSONS
import build_course as B
ROOT = Path(__file__).resolve().parent.parent

PREAMBLE = r'''\documentclass[11pt,a4paper,oneside]{report}
\input{common.tex}
\usepackage[a4paper,left=16mm,top=23mm,bottom=19mm,textwidth=132mm,marginparsep=7mm,marginparwidth=37mm,headheight=14pt]{geometry}
\usepackage{fancyhdr,enumitem,hyperref,titlesec,needspace,microtype}
\usepackage[most]{tcolorbox}
\hypersetup{colorlinks=true,linkcolor=ink,urlcolor=ink,bookmarksnumbered=true,pdfauthor={fifteen02}}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\setlist{nosep,leftmargin=1.4em}
\setcounter{tocdepth}{1}
\titleclass{\chapter}{straight}
\titleformat{\chapter}[display]{\heavy\color{ink}\raggedright}{\fontsize{9}{12}\selectfont\color{quiet}PART \thechapter}{5pt}{\fontsize{19}{23}\selectfont}
\titlespacing*{\chapter}{0pt}{14pt}{12pt}
\titleformat{\section}{\heavy\fontsize{12}{15}\selectfont\color{ink}\raggedright}{\thesection}{7pt}{}
\titlespacing*{\section}{0pt}{12pt}{4pt}
\titleformat{\subsection}{\heavy\fontsize{11}{14}\selectfont\raggedright}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{9pt}{3pt}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\fancyhead[C]{\guideheader{Lesson @NUMBER@ · @SUBTITLE@}{\nouppercase{\leftmark}}}
\fancyfoot[L]{\fontsize{8}{10}\selectfont\color{quiet}LESSON @NUMBER@\quad /\quad @SUBTITLE@}
\fancyfoot[R]{\fontsize{9}{11}\selectfont\color{quiet}\thepage}
\fancyhfoffset[R]{44mm}
\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{plain}{\fancyhf{}\fancyhead[C]{\guideheader{Lesson @NUMBER@ · @SUBTITLE@}{\nouppercase{\leftmark}}}\fancyfoot[L]{\fontsize{8}{10}\selectfont\color{quiet}LESSON @NUMBER@\quad /\quad @SUBTITLE@}\fancyfoot[R]{\fontsize{9}{11}\selectfont\color{quiet}\thepage}\renewcommand{\headrulewidth}{0pt}}
\newcommand{\classref}[1]{\marginpar{\raggedright\fontsize{9}{12}\selectfont\color{quiet}\colorbox{wash}{\heavy\fontsize{8}{10}\selectfont IN THE CLASSROOM}\par\smallskip#1}}
\newcommand{\readinggoal}[1]{\par\textbf{What we want to understand.} #1\par\smallskip}
\newcommand{\sectiongoal}[1]{\par{\color{quiet}\textbf{Objective.} #1}\par\smallskip}
\newcommand{\nextpointer}[1]{\par\smallskip{\color{quiet}\textbf{Next.} #1}\par}
\newcommand{\picturecaption}[1]{\par{\small\color{quiet}#1}\par\medskip}
\newtcolorbox{pythonnote}[1]{enhanced,colback=codepaper,colframe=codepaper,boxrule=0pt,sharp corners,borderline west={2.5pt}{0pt}{quiet},left=8pt,right=8pt,top=4pt,bottom=4pt,before skip=6pt,after skip=8pt,fontupper=\small\raggedright,title={PYTHON · #1},fonttitle=\heavy\fontsize{8}{10}\selectfont,coltitle=quiet,colbacktitle=codepaper,attach title to upper={\par\smallskip}}
\newtcolorbox{problembox}[1]{enhanced,colback=white,colframe=ink,boxrule=.6pt,arc=0pt,left=8pt,right=8pt,top=6pt,bottom=6pt,before skip=8pt,after skip=10pt,fontupper=\small,before upper={\raggedright},title={THE PROBLEM · #1},fonttitle=\heavy\fontsize{9}{11}\selectfont,coltitle=white,colbacktitle=ink}
\newtcolorbox{mainidea}{enhanced,colback=wash,colframe=wash,boxrule=0pt,sharp corners,left=10pt,right=10pt,top=8pt,bottom=8pt,before skip=6pt,after skip=10pt,before upper={\raggedright}}
\newtcblisting{bookcode}[1]{enhanced,unbreakable,listing only,listing engine=listings,colback=codepaper,frame hidden,boxrule=0pt,sharp corners,borderline west={2.5pt}{0pt}{ink!88},grow to left by=5mm,grow to right by=44mm,boxsep=0pt,left=26pt,right=12pt,top=6pt,bottom=6pt,before skip=8pt,after skip=8pt,colbacktitle=ink!88,coltitle=white,fonttitle=\heavy\fontsize{10}{13}\selectfont,titlerule=0pt,toptitle=5pt,bottomtitle=5pt,lefttitle=26pt,righttitle=12pt,title={#1\hfill{\ttfamily\fontsize{8}{10}\selectfont\color{white!60!ink}python}},listing options={language=Python,basicstyle=\ttfamily\fontsize{9.5}{13}\selectfont,breaklines=true,breakatwhitespace=true,columns=fullflexible,keepspaces=true,numbers=left,numberstyle=\ttfamily\fontsize{7.5}{13}\selectfont\color{lightink},numbersep=10pt}}
\begin{document}\color{ink}\fontsize{10.5}{13}\selectfont
'''


def btex(text):
    """B.tex with typographic quotes and arrows (Avenir has no arrow glyph)."""
    out, open_q = [], True
    for ch in str(text):
        if ch == '"':
            out.append('“' if open_q else '”'); open_q = not open_q
        else:
            out.append(ch)
    s = B.tex(''.join(out))
    s = s.replace('→', r'{\ttfamily →}').replace('←', r'{\ttfamily ←}')
    return s.replace('ⁿ', r'\textsuperscript{n}').replace('ᵐ', r'\textsuperscript{m}')


def para(text):
    return btex(text) + '\n\n'


def booktab(head, rows, spec=None, size=r'\small'):
    import re
    n = len(head)
    cols = re.sub(r'(?<!arraybackslash\})X', r'>{\\raggedright\\arraybackslash}X', spec) if spec else (r'>{\raggedright\arraybackslash}X' * n)
    lines = len(rows) + 3
    s = r'\Needspace{' + str(min(lines, 30)) + r'\baselineskip}' + '\n'
    s += r'\par\medskip\begingroup' + size + r'\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.3}'
    s += r'\begin{tabularx}{\linewidth}{' + cols + r'}\toprule' + ' & '.join(r'\textbf{' + btex(x) + '}' for x in head) + r'\\\midrule' + '\n'
    # {} stops a cell beginning with [ from being read as the optional argument of \\.
    s += ''.join('{}' + ' & '.join(btex(x) for x in row) + r'\\' + '\n' for row in rows)
    return s + r'\bottomrule\end{tabularx}\endgroup\par\medskip' + '\n'


def program(name, run):
    s = r'\Needspace{12\baselineskip}' + '\n' + r'\begin{bookcode}{' + B.tex(name.replace('_', ' ')) + '}\n' + B.precode(name).rstrip() + '\n' + r'\end{bookcode}' + '\n'
    if run:
        s += r'\Needspace{5\baselineskip}\textbf{Try it.}' + '\n' + B.listing(run)
        s += r'\textbf{Result:} ' + btex(B.example_output(run)) + '\n\n'
    if name in B.RECURSIVE:
        s += r'\textbf{Recursion depth.} ' + btex(B.RECURSION_NOTE.split(': ', 1)[1]) + '\n\n'
    return s


def problem_box(p):
    s = r'\Needspace{16\baselineskip}\begin{problembox}{' + btex(p['name']) + '}'
    for label in ('Story', 'Rules', 'Input', 'Output', 'Limits'):
        if p.get(label.lower()):
            text = p[label.lower()]
            s += r'\textbf{' + label + '.} ' + btex(text[:1].upper() + text[1:]) + r'\par\smallskip '
    s += r'\textbf{Example input.}' + B.listing(p['example_in']).replace(r'\begin{lstlisting}', r'\begin{lstlisting}[language={},aboveskip=2pt,belowskip=2pt]')
    s += r'\textbf{Expected output:} ' + btex(p['example_out']) + r'\par\smallskip ' + btex(p['why'])
    s += r'\par\smallskip\textbf{Source.} ' + btex(p['source'])
    if p.get('url'):
        s += r'\par\url{' + p['url'] + '}'
    return s + r'\end{problembox}' + '\n'


def judge(fn, n):
    path = ROOT / f'Lesson {n}' / 'programs' / f'{fn}.py'
    expected = B.precode(fn) + '\n' + B.WRAPPERS[fn]
    # The book prints exactly what build_course writes to programs/ (verify_books.py checks the file).
    return r'\Needspace{14\baselineskip}\begin{bookcode}{programs/' + B.tex(fn) + '.py}\n' + expected.rstrip() + '\n' + r'\end{bookcode}' + '\n'


def block(b, n, units):
    if isinstance(b, str):
        return para(b)
    typ = b[0]
    if typ == 'code':
        return program(b[1], b[2])
    if typ == 'table':
        return booktab(b[1], b[2], b[3] if len(b) > 3 else None)
    if typ == 'diagram':
        u = units[b[1]]
        return r'\Needspace{10\baselineskip}' + '\n' + B.diagram(u.get('answer_diagram') or u['diagram'])
    if typ == 'figure':
        return r'\Needspace{12\baselineskip}\begin{center}' + b[1] + r'\end{center}\picturecaption{' + btex(b[2]) + '}\n'
    if typ == 'pause':
        return (r'\Needspace{8\baselineskip}\begin{tcolorbox}[before upper={\raggedright},before lower={\raggedright},fontupper=\small,fontlower=\small,colback=white,colframe=ink,boxrule=.6pt,arc=0pt,title={AT THE BOARD},fonttitle=\heavy,coltitle=white,colbacktitle=ink]'
                + btex(b[1]) + r'\tcblower\textbf{Reasoning.} ' + btex(b[2]) + r'\end{tcolorbox}' + '\n')
    if typ == 'python':
        return r'\Needspace{6\baselineskip}\begin{pythonnote}{' + btex(b[2]) + '}' + btex(b[3]).replace('\n\n', r'\par\smallskip ') + r'\end{pythonnote}' + '\n'
    if typ == 'problem':
        return problem_box(b[1])
    if typ == 'cost':
        title, head, rows = b[1], b[2], b[3]
        return r'\Needspace{' + str(len(rows) * 2 + 6) + r'\baselineskip}\textbf{' + btex(title) + '}\n' + booktab(head, rows, r'>{\raggedright\arraybackslash}p{8mm}>{\raggedright\arraybackslash}p{40mm}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}p{17mm}>{\raggedright\arraybackslash}p{20mm}', r'\footnotesize')
    if typ == 'items':
        return r'\begin{itemize}' + ''.join(r'\item ' + btex(x) for x in b[1]) + r'\end{itemize}' + '\n'
    if typ == 'recap':
        return r'\Needspace{6\baselineskip}\par\medskip{\heavy Recap}\par' + block(('items', b[1]), n, units)
    if typ == 'listing':
        return r'\Needspace{5\baselineskip}' + B.listing(b[1]).replace(r'\begin{lstlisting}', r'\begin{lstlisting}[language={}]')
    if typ == 'judge':
        return judge(b[1], n)
    raise ValueError(typ)


def estimate(b):
    """Rough height of a block in lines, so a heading is never left without its first block."""
    if isinstance(b, str):
        return min(len(b) // 75 + 1, 8)
    typ = b[0]
    if typ in ('table', 'cost'):
        rows = b[2] if typ == 'table' else b[3]
        return min(int(len(rows) * 1.6) + 4, 24)
    if typ == 'code':
        return min(len(__import__('build_course').precode(b[1]).splitlines()) + 4, 26)
    return {'figure': 14, 'problem': 22, 'pause': 8, 'python': 7, 'diagram': 10, 'judge': 18}.get(typ, 6)


def section_tex(sec, n, units):
    bl = sec['blocks']
    first = estimate(bl[0]) if bl else 4
    if bl and isinstance(bl[0], str) and len(bl) > 1:
        first += min(estimate(bl[1]), 12)
    s = r'\Needspace{' + str(min(6 + first, 30)) + r'\baselineskip}' + '\n' + r'\section{' + btex(sec['title']) + '}\n'
    if sec['ids']:
        s += r'\classref{' + r'\\'.join(sec['ids']) + '}\n'
    s += r'\sectiongoal{' + btex(sec['goal']) + '}\n'
    for b in sec['blocks']:
        s += block(b, n, units)
    if sec.get('next'):
        s += r'\nextpointer{' + btex(sec['next']) + '}\n'
    return s


def chapter_tex(ch, n, units):
    s = r'\Needspace{22\baselineskip}' + '\n' + r'\chapter{' + btex(ch['title']) + '}\n' + r'\readinggoal{' + btex(ch['goal']) + '}\n'
    for b in ch.get('opening', ()):
        s += block(b, n, units)
    for sec in ch['sections']:
        s += section_tex(sec, n, units)
    return s


def front(L, book):
    s = r'\chapter*{The route through this book}\addcontentsline{toc}{chapter}{The route through this book}\markboth{The route through this book}{}' + '\n'
    s += r'\begin{mainidea}{\color{quiet}\heavy\fontsize{9}{11}\selectfont MAIN IDEA OF LESSON ' + str(L['n']) + r'}\par\smallskip{\heavy\fontsize{17}{21}\selectfont ' + btex(L['title']) + r'.}\par\smallskip ' + btex(book['idea']) + r'\end{mainidea}' + '\n'
    s += para(book['intro'])
    s += r'\textbf{After this lesson you will be able to}' + block(('items', book['outcomes']), L['n'], {})
    s += r'\Needspace{6\baselineskip}\textbf{The route}\par' + '\n'
    for i, ch in enumerate(book['chapters'], 1):
        title = ch['title'] if ch['title'][-1] in '?.!' else ch['title'] + '.'
        s += r'\textbf{' + str(i) + '. ' + btex(title) + r'} ' + btex(ch['goal']) + r'\par' + '\n'
    s += r'\textbf{' + str(len(book['chapters']) + 1) + r'. Run, test and explain your program.} ' + btex('Use the starter file, the test files and the runner; read every edge file.') + r'\par' + '\n'
    for b in book.get('front', ()):
        s += block(b, L['n'], {})
    return s


def render(L):
    n = L['n']; book = BOOKS[n]
    s = PREAMBLE.replace('@NUMBER@', str(n)).replace('@SUBTITLE@', B.tex(L['subtitle']))
    s += B.cover(L, 'tutorial')
    s += front(L, book)
    s += r'\clearpage\tableofcontents\clearpage' + '\n'
    units = {u['id']: u for u in L['units']}
    for ch in book['chapters']:
        s += chapter_tex(ch, n, units)
    s += practice(L)
    if book.get('appendix'):
        s += r'\appendix' + '\n'
        for ch in book['appendix']:
            s += chapter_tex(ch, n, units)
    s += r'\end{document}' + '\n'
    return s


def practice(L):
    from make_practice import SPECS, INFO, datasets, size_detail
    import random
    n = L['n']; names = [p for p, *_ in SPECS[n]]; problem = names[0]
    s = r'\Needspace{22\baselineskip}' + '\n' + r'\chapter{Run, test and explain your program}' + '\n'
    s += r'\readinggoal{Use file-based tests without mixing input handling with the algorithm.}' + '\n'
    s += section_tex(dict(title='The files students work with', ids=[], goal='Know which file holds what, and which files students receive.', blocks=[
        'Open starter.py. Each problem has a function with the same signature as the lesson and a description of what it must return. The input reading and tests are already provided by runner.py. Students replace the unfinished function body with their own algorithm. They return the answer from the function; the runner prints and checks it. The separate solution.py contains completed iterative implementations for the tutor.',
        ('table', ['File or folder', 'Purpose'], [['starter.py', 'Student function skeletons; no imported solutions.'], ['runner.py', 'Read inputs, call a function and compare its answer.'], ['test-cases/', 'Plain .in files and matching expected .out files.'], ['solution.py', 'Separate completed solutions for the tutor.'], ['PRACTICE.txt', 'Commands, formats and dataset sizes for this lesson.'], ['programs/', 'Complete programs for the original judges.']], r'>{\raggedright\arraybackslash}p{30mm}X'),
        'The student download includes starter.py, runner.py and test-cases/, but excludes solution.py, solutions.py and the teacher notebook. Expected outputs are provided so students can check their work; an output number is not a solution algorithm.'],
        next='Run the small tests first.'), n, {})
    blocks = ['From the lesson folder, run the commands below in a terminal. These are terminal commands, not Python statements to paste inside a function. The first command runs the small and edge cases for every problem in this lesson. The second runs only one named problem.',
              ('listing', 'python3 starter.py\npython3 starter.py --problem ' + problem + ' --size small'),
              'An unfinished function raises NotImplementedError and is reported as NOT IMPLEMENTED. It does not pass the test. Once the function is implemented, PASS means its returned answer matches the expected .out file. A wrong result is reported with the expected and actual values. A recursion error is identified separately from a wrong answer.',
              'Each problem has its own folder beneath test-cases/, named as in the table. Open a small .in file and its matching .out file side by side, work the instance by hand, then run it. The runner turns each file into the arguments of the named function, so the function never reads input itself.',
              ('table', ['Folder', 'Input file', 'Answer in the .out file'], [[p, INFO[p]['format'], INFO[p]['answer']] for p in names], r'>{\raggedright\arraybackslash}p{20mm}XX'),
              'The runner locates its default test suite beside its own file. It works even if the terminal is currently in another folder. With `--file`, the supplied path is interpreted relative to the terminal\'s current folder. The matching expected answer is the same filename with .out instead of .in.',
              ('listing', 'python3 starter.py --problem ' + problem + ' --file test-cases/' + problem + '/small.in')]
    s += section_tex(dict(title='Begin with a small test', ids=[], goal='Run one problem on its small file and read the result.', blocks=blocks, next='Move to the larger files once the small and edge files pass.'), n, {})
    rows = [[p] + [size_detail(p, args) for args in datasets(p, random.Random(261024))] for p in names]
    blocks = ['Small cases expose the meaning of the state and the starting values, and can be checked by hand. Medium and large cases exercise the iterative method at a substantial input size; a correct but slow method shows up as a timeout there.',
              'Python stops recursion at about 1,000 nested calls by default. The recursive versions in this lesson, cached or not, are therefore for small inputs and the small and edge files only. On the medium and large files a recursive version may stop with RECURSION LIMIT or run out of time; use the iterative version for those.',
              ('listing', 'python3 starter.py --size medium\npython3 starter.py --size large\npython3 solution.py --size all'),
              ('table', ['Problem', 'Small', 'Medium', 'Large'], rows, r'>{\raggedright\arraybackslash}p{20mm}XXX'),
              'Each edge file tests one boundary of the rules. They run with the small suite.',
              ('table', ['Edge file', 'What it tests'], [[f'{p}/edge-{i}.in', text] for p in names for i, text in enumerate(INFO[p]['edges'], 1)], r'>{\raggedright\arraybackslash}p{34mm}X'),
              'The runner allows 30 seconds per case and runs each case in a separate process. A timeout stops that case and permits the rest of the suite to continue. Use `--timeout 60` if a slower machine needs more time.',
              'A passing file is evidence for that input, not a proof for all inputs. The chapter reasoning explains why the recurrence covers every legal choice. The test suite checks that the implementation follows that reasoning on concrete cases. The expected outputs were cross-checked using independently formulated algorithms or exact bounds. Runtime reports include process startup and should not be treated as online-judge timing guarantees.']
    s += section_tex(dict(title='Move from small to medium to large', ids=[], goal='Use each dataset size for its purpose and know what every edge file checks.', blocks=blocks, next='Connect the files with the other lesson materials.'), n, {})
    blocks = ['Use the teacher guide for the timed lesson route and short prompts. Use the worksheet for students\' traces and explanations. The slide deck presents a question before its answer. The notebook provides an alternative to a local editor and includes worked examples plus exercise cells. These are different ways to practise the same ideas, not separate algorithms to learn.',
              'A useful final check is to ask a student to explain one table entry, one transition and one boundary case without reading the code. If those are clear, a failing test can be investigated by tracing the first state where the program and the hand calculation disagree.']
    s += section_tex(dict(title='Connect the files to the classroom', ids=[], goal='Choose the right material for each part of the lesson.', blocks=blocks, next=BOOKS[n].get('practice_next', 'The appendix collects the summary tables for quick reference.')), n, {})
    return s


def build():
    for L in LESSONS:
        from compile_all import source_path
        path = source_path(L['n'], 'tutorial')
        path.write_text(render(L))
        print(f'Wrote {path}')


if __name__ == '__main__':
    build()
