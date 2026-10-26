import dice_memory as DM
import frog_graph as FG
from pathlib import Path
import inspect, json, re, shutil, io, contextlib, pprint, sys, zipfile, base64
import content as C
import programs as P
from sheet_guidance import GUIDES, CODING, TABLES, TABLE_ANSWERS, part
from classroom_layout import NUMBERED_STYLE, numbered, call_text, ruled, code_slides
import starting_points as SP
import recursion_intro as RI
from sheet_guidance import IMPLEMENT
from slide_illustrations import illustrated_body
import warm_slides as WARM
import cohesive_slides as COH
ROOT=Path(__file__).resolve().parent.parent
HERE=Path(__file__).resolve().parent
FONT=ROOT/'Lesson 1/fonts'
# All original problem statements have been distributed into this local source.
BRIEFS=json.loads((HERE/'problem_briefs.json').read_text())
GROUPS={1:[0],2:[1,2],3:[3,4],4:[5],5:[6]}
FUNCTIONS={1:['frog_table'],2:['dice_table','grid_table'],3:['tower_table','array_rolling'],4:['feast_table'],5:['hps_table']}
WRAPPERS={
'frog_table':"n = int(input())\nheights = list(map(int, input().split()))\nprint(frog_table(heights))\n",
'dice_table':"n = int(input())\nprint(dice_table(n))\n",
'grid_table':"n = int(input())\nrows = [input().strip() for _ in range(n)]\nprint(grid_table(rows))\n",
'tower_table':"tests = int(input())\nfor _ in range(tests):\n    n = int(input())\n    bosses = list(map(int, input().split()))\n    print(tower_table(bosses))\n",
'array_rolling':"n, m = map(int, input().split())\nvalues = list(map(int, input().split()))\nprint(array_rolling(values, m))\n",
'feast_table':"with open('feast.in') as source:\n    limit, a, b = map(int, source.read().split())\nanswer = feast_table(limit, a, b)\nwith open('feast.out', 'w') as target:\n    target.write(str(answer) + '\\n')\n",
'hps_table':"with open('hps.in') as source:\n    words = source.read().split()\nn, budget = map(int, words[:2])\njohn = words[2:]\nanswer = hps_table(john, budget)\nwith open('hps.out', 'w') as target:\n    target.write(str(answer) + '\\n')\n"}

def esc(t):
    s=''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#','%':r'\%','_':r'\_','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in str(t))
    # LaTeX turns -- into an en dash; keep command flags such as --file copyable.
    while '--' in s: s=s.replace('--','-{}-')
    return s
def tex(t):
    parts=str(t).split('`')
    return ''.join((r'\texttt{'+esc(x)+'}') if i%2 else esc(x) for i,x in enumerate(parts)).replace('\n\n','\n\n')
def codes(u): return ([u['code']] if isinstance(u.get('code'),str) else u.get('code')) or []
def precode(name):
    s=inspect.getsource(getattr(P,name))
    pre=''
    if 'sys.' in s: pre+='import sys\n\n'
    if '@lru_cache' in s: pre+='from functools import lru_cache\n\n'
    if 'MOD' in s: pre+='MOD = 1_000_000_007\n\n'
    if 'BEATS' in s: pre+="BEATS = {'H': 'S', 'P': 'H', 'S': 'P'}\n\n"
    return pre+s

# Recursive classroom versions (cached or not). Python's default recursion limit
# is about 1,000 nested calls, so these are for small inputs and edge files only.
RECURSIVE={'stairs_slow','stairs_cached','frog_slow','frog_cached','dice_slow','dice_cached','grid_slow','grid_cached','tower_cached','array_cached','feast_cached','hps_cached'}
RECURSION_NOTE='Recursion depth: Python stops recursion at about 1,000 nested calls by default, so this recursive version is for small inputs and the small and edge test files only. Use the iterative version for the medium and large files.'

def lesson_functions(L):
    functions=list(dict.fromkeys(fn for u in L['units'] for fn in codes(u)))
    if L['n']==1:
        functions=list(dict.fromkeys(['countdown','sum_to','sum_squares']+functions))
    for e in L['exercises']:
        if e['solution'] not in functions: functions.append(e['solution'])
    return functions

def constants_for(names,imports=True):
    """Only the imports and constants that the named functions actually use."""
    src='\n'.join(inspect.getsource(getattr(P,f)) for f in names)
    head=''
    if imports and 'sys.' in src: head+='import sys\n'
    if imports and '@lru_cache' in src: head+='from functools import lru_cache\n'
    if 'MOD' in src: head+='MOD = 1_000_000_007\n'
    if 'BEATS' in src: head+="BEATS = {'H': 'S', 'P': 'H', 'S': 'P'}\n"
    return head

def setup_code(L):
    return constants_for(lesson_functions(L))+"print('Ready. Run cells from top to bottom.')\n"

# Student-notebook stubs for program-writing questions: docstring and small checks.
# Expected values are computed from the reference functions when the notebook is built.
STUBS={
'power2':('For a nonnegative integer n, return 2 to the power n. Repair the missing stopping case before testing.',['(0,)','(1,)','(3,)','(6,)']),
'factorial':('Return n! = 1 x 2 x ... x n, with factorial(0) = 1. Use recursion: the base case first, then one smaller call.',['(0,)','(1,)','(4,)','(6,)']),
'stairs_13':('Return the number of routes to step n when each move climbs exactly 1 or 3 steps. Fill a list in increasing order.',[]),
'frog_table':('Return the cheapest total cost from stone 0 to the last stone, filling best[i] from left to right.',[]),
'frog_path':('Return (cost, path) for a nonempty height list. path contains stone indices from start to finish. Save a predecessor with each best cost; on equal costs keep i - 1.',['([20, 50, 30, 40, 10, 10],)','([10, 30, 20, 40],)','([7],)']),
'dice_123':('Return the number of ordered sequences of 1, 2 and 3 with total n, modulo MOD, filling ways[0..n] in increasing order.',[]),
'tower_table':('bosses lists 0 (easy) and 1 (hard). Return the least total your friend pays, filling friend[i] and you[i] from the last boss back to the first.',[]),
'array_rolling':('values holds fixed entries and 0 for missing ones; fill each 0 with 1..m so that neighbours differ by at most 1. Return the number of fillings modulo MOD, keeping only the previous row of counts.',[]),
'stairs_slow':('Return the number of routes to step n with jumps of 1 or 2. Use plain recursion: stopping cases first, then the two possible last jumps.',['(1,)','(3,)','(5,)']),
'stairs_table':('Return the number of routes to step n with jumps of 1 or 2. Fill a list ways[0..n] with a loop, in increasing order.',['(0,)','(1,)','(5,)','(40,)']),
'frog_slow':('Return the cheapest total cost from stone 0 to the last stone. cost(i) tries both possible last jumps recursively.',['([10, 30, 20, 40],)','([20, 50, 30, 40, 10, 10],)']),
'dice_slow':('Return the number of ordered sequences of faces 1 to 6 with total n. Plain recursion; use small n only.',['(0,)','(3,)','(4,)']),
'dice_cached':('Return the same count as dice_slow, saving each total in a dictionary. Store counts modulo MOD.',['(4,)','(7,)','(50,)']),
'dice_table':('Return the dice count for total n, modulo MOD, by filling ways[0..n] in increasing order.',['(4,)','(7,)','(1000,)']),
'grid_cached':("rows is a list of n strings of '.' (open) and '*' (blocked). Return the number of right/down paths from the top-left cell to the bottom-right cell, modulo MOD, using a cached recursive count(r, c).",["(['...', '.*.', '...'],)","(['..', '..'],)","(['*'],)"]),
'grid_table':('Return the same path count as grid_cached, filling paths[r][c] row by row with a loop, modulo MOD.',["(['...', '.*.', '...'],)","(['..', '..'],)","(['.'],)"]),
'tower_cached':('bosses lists 0 (easy) and 1 (hard). Your friend moves first; each turn takes the next 1 or 2 bosses; your friend pays 1 for each hard boss on their own turns. Return the least total your friend pays, using a cached recursive cost(i, friend_turn).',['([1, 0, 1, 1],)','([1],)','([1, 1, 1],)']),
'array_cached':('values holds fixed entries and 0 for missing ones. Fill each 0 with 1..m so that neighbours differ by at most 1. Return the number of fillings modulo MOD, using a cached recursive count(i, previous).',['([2, 0, 0, 1], 3)','([0], 3)','([1, 3], 3)']),
'feast_cached':('Return the greatest fullness reachable without exceeding limit, eating fruit a or b any number of times and drinking water (fullness // 2) at most once. Use a cached recursive best(fullness, used_water).',['(10, 4, 7)','(9, 4, 6)','(15, 8, 9)']),
'feast_table':('Return the same answer as feast_cached with three passes over two bytearrays, dry and wet: eat before water, drink once, then eat after water.',['(10, 4, 7)','(15, 8, 9)','(10000, 2527, 2945)']),
'hps_cached':('john is a string of H, P and S. Return the most rounds you can win with at most budget switches; the first gesture is free. Use a recursive best(i, left, previous).',["('HHSSP', 1)","('HPS', 0)","('SSPPH', 2)"]),
'hps_table':('Return the same answer as hps_cached, keeping only the previous round: before[used][g] and a fresh now table for each round.',["('HHSSP', 1)","('HHSSP', 0)","('SSPPH', 2)"]),
}
# Shown nowhere in the student notebook (an uncached alternative that would pass an exercise).
STUDENT_HIDE={'grid_slow'}

def given_code(u):
    """Code printed with a question: a programs.py function, or literal code to repair."""
    g=u['given']
    return inspect.getsource(getattr(P,g)) if hasattr(P,g) else g

# Explicit teaching links: matching a few test outputs does not make two
# different implementations the same program (for example cached vs iterative).
DEFERRED_CODE = {
    (3, 'tower_table'): 'L3-06',
    (3, 'array_full'): 'L3-12',
    (3, 'array_rolling'): 'L3-12',
}

def solves_exercise(L,fn):
    target = DEFERRED_CODE.get((L['n'], fn))
    return next((ex for ex in L['exercises'] if ex['id'] == target), None)


def student_mode(L,u,fn):
    from sheet_guidance import CODING
    if fn in STUDENT_HIDE: return 'skip'
    if u['id'] in IMPLEMENT: return 'stub'
    if solves_exercise(L,fn): return 'hidden'
    return 'example'

def stub_source(fn):
    """Exact signatures from solutions.py, nested functions included; returns None."""
    return SP.stub(fn,STUBS[fn][0])

def check_cell(fn,cases,done='All checks passed.'):
    """Checks written as ordinary calls, e.g. frog_table([10, 30, 20, 40])."""
    for args,want in cases: assert eval(call_text(fn,args),NS(fn))==want,(fn,args)
    rows=''.join(f'    ({call_text(fn,args)}, {want!r}),\n' for args,want in cases)
    return (f"checks = [\n{rows}]\nif any(actual is None for actual, expected in checks):\n    print('Not implemented yet. Complete the function above.')\n"
            f"else:\n    for number, (actual, expected) in enumerate(checks, 1):\n        assert actual == expected, ('check', number, 'expected', expected, 'got', actual)\n    print('{done}')\n")

def NS(fn):
    """Namespace in which each exercise name calls its reference solution."""
    ns=vars(P).copy()
    for L in C.LESSONS:
        for ex in L['exercises']: ns[ex['function']]=getattr(P,ex['solution'])
    return ns

def stub_cases(fn):
    return [(args,eval(fn+args,vars(P).copy())) for args in STUBS[fn][1]]

def example_output(run):
    out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(run,vars(P).copy())
    return out.getvalue().strip()

from candies_style import COMMON, cover, colab_link, assets as style_assets

def bookhead(L,kind):
    return r'''\documentclass[11pt,a4paper]{article}
\input{common.tex}
\usepackage[a4paper,left=16mm,right=18mm,top=24mm,bottom=19mm,headheight=14pt]{geometry}
\usepackage{fancyhdr,enumitem,hyperref}
\hypersetup{colorlinks=true,linkcolor=teal,urlcolor=teal}
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt}
\setlist{nosep,leftmargin=1.4em}
\usepackage{needspace,colortbl}
@STYLE@
\pagestyle{fancy}\fancyhf{}
\fancyhead[C]{\guideheader{Lesson @NUMBER@ · @SUBTITLE@}{@KIND@ · \nouppercase{\leftmark}}}
\fancyfoot[L]{\fontsize{8}{10}\selectfont\color{quiet}LESSON @NUMBER@ / @SUBTITLE@}
\fancyfoot[R]{\fontsize{9}{11}\selectfont\color{quiet}\thepage}
\renewcommand{\headrulewidth}{0pt}
\newcommand{\topic}[2]{\clearpage\markboth{#2}{}{\color{quiet}\fontsize{9}{12}\selectfont\textbf{#1}}\par{\heavy\fontsize{19}{23}\selectfont\raggedright #2\par}\vspace{5pt}}
\newcommand{\topicflow}[2]{\par\Needspace{20\baselineskip}\bigskip\markboth{#2}{}{\color{quiet}\fontsize{9}{12}\selectfont\textbf{#1}}\par{\heavy\fontsize{19}{23}\selectfont\raggedright #2\par}\vspace{5pt}}
\newcommand{\labeltext}[1]{{\color{teal}\textbf{#1}}\par}
\begin{document}\color{ink}\fontsize{10.5}{13}\selectfont
'''.replace('@STYLE@',NUMBERED_STYLE).replace('@NUMBER@',str(L['n'])).replace('@SUBTITLE@',tex(L['subtitle'])).replace('@KIND@',kind.title())


def tab(d,question=False,slide=False):
    rows=d.get('blank') if question and d.get('blank') else d['rows']
    n=len(d['head'])
    size=r'\fontsize{18}{22}\selectfont' if slide and n<9 and len(rows)<5 else (r'\fontsize{15}{18}\selectfont' if slide else (r'\footnotesize' if n>9 else r'\small'))
    # Width-controlled table. Headings and cells can wrap.
    # A long row label in a wide table gets a natural-width first column.
    first=r'>{\raggedright\arraybackslash}l' if n>=7 and max(len(str(r[0])) for r in [d['head']]+rows)>=9 else r'>{\raggedright\arraybackslash}X'
    # A cell starting with [ would be read as the optional argument of \\ or \midrule.
    cell=lambda x: ('{}' if str(x).startswith('[') else '')+tex(x)
    return r'\begingroup'+size+r'\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.35}\begin{tabularx}{\linewidth}{'+first+(r'>{\raggedright\arraybackslash}X'*(n-1))+r'}\toprule'+' & '.join(r'\textbf{'+tex(x)+'}' for x in d['head'])+r'\\\midrule'+'\n'+''.join(' & '.join(cell(x) for x in row)+r'\\'+'\n' for row in rows)+r'\bottomrule\end{tabularx}\endgroup'

def diagram(d,question=False,slide=False):
    if not d: return ''
    if d['kind']=='table': return r'\par\medskip '+tab(d,question,slide)+r'\par\medskip '
    if question and d['kind'] not in ('tree','lastmove'): return ''
    prefix=r'\begin{center}\begin{tikzpicture}[>=Stealth,every node/.style={font=\small},box/.style={draw=teal,rounded corners,minimum width=20mm,minimum height=8mm,fill=wash},arr/.style={->,thick,teal}]'
    body=''
    if d['kind']=='lastmove':
        if question:
            body=r'\node[box] (a) at (0,1) {step ?};\node[box] (b) at (0,-1) {step ?};\node[box] (c) at (8,0) {step 5};\draw[arr] (a)--node[above,sloped]{final jump of 1}(c);\draw[arr] (b)--node[below,sloped]{final jump of 2}(c);'
        else:
            body=r'\node[box] (a) at (0,1) {step 4};\node[box] (b) at (0,-1) {step 3};\node[box] (c) at (8,0) {step 5};\draw[arr] (a)--node[above,sloped]{5 routes, then jump 1}(c);\draw[arr] (b)--node[below,sloped]{3 routes, then jump 2}(c);'
    if d['kind']=='tree':
        for key,x,y,label in [('a',5,0,'ways(5)'),('b',2.5,-1.3,'ways(4)'),('c',7.5,-1.3,'ways(3)'),('d',1,-2.6,'ways(3)'),('e',4,-2.6,'ways(2)'),('f',6.5,-2.6,'ways(2)'),('g',9.5,-2.6,'ways(1)')]:
            fill='paper' if question or key not in ('c','d') else 'wash'
            body+=r'\node[box,fill='+fill+'] ('+key+') at ('+str(x)+','+str(y)+r') {\texttt{'+label+'}};'
        for a,b in [('a','b'),('a','c'),('b','d'),('b','e'),('c','f'),('c','g')]: body+=rf'\draw[arr] ({a})--({b});'
    if d['kind']=='feastpath':
        for i,value in enumerate([0,7,3,10]): body+=rf'\node[box] (p{i}) at ({i*3.6},0) {{{value}}};'
        for i,label in enumerate(['eat 7','water: // 2','eat 7']): body+=rf'\draw[arr] (p{i})--node[above=6mm]{{{label}}}(p{i+1});'
    if d['kind']=='waterlayers':
        body=r'\node[anchor=east] at (-1,0) {dry};\node[anchor=east] at (-1,-2) {just drank};'
        for i,(a,b) in enumerate(zip([0,4,7,8],[0,2,3,4])):
            body+=rf'\node[box] (a{i}) at ({i*2.8},0) {{{a}}};\node[box] (b{i}) at ({i*2.8},-2) {{{b}}};\draw[arr,orange] (a{i})--node[right]{{// 2}}(b{i});'
    if d['kind']=='gridroutes':
        size=1.5
        for r in range(3):
            for c in range(3):
                x,y=c*size,-r*size
                blocked=(r,c)==(1,1)
                body+=rf'\draw[teal,fill={"wash" if blocked else "paper"}] ({x-size/2},{y-size/2}) rectangle ({x+size/2},{y+size/2});'
                body+=rf'\node[anchor=north west,inner sep=2pt,font=\scriptsize,text=quiet] at ({x-size/2},{y+size/2}) {{{r},{c}}};'
        body+=rf'\node[font=\Large,text=quiet,inner sep=0pt] at ({size},{-size+0.1}) {{*}};\node[font=\scriptsize,text=quiet,inner sep=0pt] at ({size},{-size-0.4}) {{blocked}};'
        body+=rf'\node[anchor=south] at (0,{size/2}) {{start}};\node[anchor=north] at ({2*size},{-2*size-size/2}) {{finish}};'
        # Route 1 along the top row and right column; route 2 down the left column and along the bottom.
        for (x0,y0),(x1,y1) in [((0,0),(1,0)),((1,0),(2,0)),((2,0),(2,1)),((2,1),(2,2))]:
            body+=rf'\draw[arr,line width=1.6pt,shorten >=3pt,shorten <=3pt] ({x0*size},{-y0*size})--({x1*size},{-y1*size});'
        for (x0,y0),(x1,y1) in [((0,0),(0,1)),((0,1),(0,2)),((0,2),(1,2)),((1,2),(2,2))]:
            body+=rf'\draw[arr,orange,dashed,line width=1.6pt,shorten >=3pt,shorten <=3pt] ({x0*size},{-y0*size})--({x1*size},{-y1*size});'
        for (x,y) in [(0,0),(2,2)]: body+=rf'\fill[teal] ({x*size},{-y*size}) circle (3pt);'
        lx=3*size+0.3
        body+=rf'\draw[arr,line width=1.6pt] ({lx},{-0.4})--({lx+1.2},{-0.4});\node[anchor=west] at ({lx+1.3},{-0.4}) {{Route 1: right, right, down, down}};'
        body+=rf'\draw[arr,orange,dashed,line width=1.6pt] ({lx},{-1.3})--({lx+1.2},{-1.3});\node[anchor=west] at ({lx+1.3},{-1.3}) {{Route 2: down, down, right, right}};'
        body+=rf'\node[anchor=north west,text width=62mm,inner sep=0pt] at ({lx},{-2.0}) {{Every other route enters the blocked centre (1,1). Cells are labelled row, column.}};'
    if slide: prefix=prefix.replace('font=\\small',r'font=\fontsize{13}{15}\selectfont')
    return prefix+body+r'\end{tikzpicture}\end{center}'

def plan(L):
    s=r'\topic{BEFORE CLASS}{The lesson route}'+'\n'
    s+=main_idea_box(L)+'\n\n'
    s+='The target is understanding, not finishing every page. Use the question IDs to move between slides, worksheet and notebook.'+(' Questions labelled optional are extensions.' if any(u['extension'] for u in L['units']) else '')+'\n\n'
    s+=tab(dict(head=['Minutes','Activity','Question IDs'],rows=[[a,b,((' to '.join(f'L{L["n"]}-'+part for part in c.split('-'))) if c else '')] for a,b,c in L['plan']]))
    s+='\n\n'+r'\labeltext{Pacing and preparation}'+'\n'
    s+='Ask students to predict before running code. Allow a quiet individual attempt before asking for a volunteer. If an answer is wrong, trace the first state where it differs. Keep the final ten minutes for explanation and questions. Move an unfinished implementation to the next session rather than shortening the reasoning.\n\n'
    s+='Students need Python functions, lists, loops, indexing, comparisons and basic arithmetic. Introduce new syntax beside the program that uses it. Use small inputs for uncached recursion; the notebook never starts an enormous recursive run. Python stops recursion at about 1,000 nested calls by default, so every recursive version in this lesson, cached or not, is for small inputs and the small and edge test files only. The medium and large files are for the iterative versions.\n\n'
    if L['n']==1: s+='L1-21 adds route recovery after the cost solution. Allow 15-20 extra minutes or use it as a follow-up; it is outside the two-hour core.\n\n'
    if L['n']==2: s+='The final five minutes can introduce L2-08: why only six Dice counts are needed. Allow 15-20 minutes in a follow-up to trace the circular buffer and running sum in full.\n\n'
    s+='Open lesson.ipynb in Jupyter or upload it to Google Colab, choose a Python 3 runtime, and run the setup cell first. Shift+Enter runs a cell. Restart and run from the top if names or data become stale. The notebook needs only Python standard-library features and no local files.\n'
    return s

def main_idea_box(L):
    """The lesson's main idea and outcomes, in the words used with students (also slide 2)."""
    return (r'\par\noindent\colorbox{wash}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{\vspace{3pt}{\color{quiet}\heavy\fontsize{8.5}{10}\selectfont MAIN IDEA: SAY THIS AT THE START}\par\smallskip'
            r'{\heavy\fontsize{15}{18}\selectfont '+tex(L['title'])+r'.}\par\smallskip '+tex(L['idea'])+r'\par\medskip\textbf{By the end of the lesson you will be able to}'
            r'\begin{itemize}'+''.join(r'\item '+tex(x) for x in L['able'])+r'\end{itemize}\vspace{3pt}}}\par')

def sources(L):
    s=r'\topic{REFERENCE}{Where the problems come from}'+'\n'
    s+='Problem statements in this course are retold for teaching. The links below lead to the original statements. Classroom examples may differ from the official samples.\n\n'
    for title,url in L['sources']:
        s+=r'\textbf{'+tex(title)+'}\\\n'+(r'\url{'+url+'}' if url.startswith('http') else tex(url))+'\\par\\medskip\n'
    return s

def briefs(L):
    s=''
    for idx in GROUPS[L['n']]:
        title,level,story,rules,inp,outp,limits,example,answer,why,judge,url,hint=BRIEFS[idx]
        s+=r'\topic{PROBLEM STATEMENT}{'+tex(title)+'}\n'+rules+'\n\n'+r'\textbf{Input.} '+inp+'\n\n'+r'\textbf{Output.} '+outp+'\n\n'+r'\textbf{Limits.} '+limits+'\n\n'+r'\textbf{Classroom example input}\begin{lstlisting}[language={}]'+'\n'+example+'\n'+r'\end{lstlisting}'+'\n'+r'\textbf{Answer:} '+tex(answer)+'. '+why+'\n\n'+r'\textbf{Original source:} '+tex(judge)+r'\par\url{'+url+'}\n'
    return s

def listing(code): return '\n'+r'\begin{lstlisting}'+'\n'+code.rstrip()+'\n'+r'\end{lstlisting}'+'\n'

def tutorial(L):
    from build_books import render
    return render(L)


def teacher(L):
    s=bookhead(L,'teacher')+cover(L,'teacher',colab=True)+plan(L)
    s+=reference(L)
    # Questions flow: each one stays whole, and a page holds as many as fit.
    s+=r'\topicflow{IN CLASS}{Questions, answers and prompts}'+'\n'
    if L['n']==1: s+=RI.teacher(tex,ruled,listing)
    current=None
    for i,u in enumerate(L['units'],1):
        topic=part(L['n'],i)
        if topic!=current:
            if current is not None: s+=r'\Needspace{14\baselineskip}'
            s+=r'\markboth{'+tex(topic)+r'}{}{\color{quiet}\heavy\fontsize{10}{13}\selectfont '+tex(topic.upper())+r'}\par\medskip'+'\n'
            current=topic
        s+=r'\noindent\begin{minipage}{\textwidth}'+'\n'+r'{\color{teal}\textbf{'+u['id']+(' / OPTIONAL' if u['extension'] else '')+'}}\\quad '+r'\textbf{'+tex(u['title'])+'}\\par\\smallskip\n'
        s+=r'\textbf{Ask.} '+tex(u['q'])+'\\par\\smallskip\n'
        if u.get('given'): s+=r'{\small\textbf{Code printed with the question.}}'+SP.code_tex(given_code(u).rstrip().splitlines(),tex)+r'\smallskip'
        if u['id'] in IMPLEMENT: s+=SP.print_tex(u['id'],tex,'Students start with:','Hints to give, one at a time.')
        s+=r'\textbf{Answer.} '+tex(u['a'])+'\\par\\smallskip\n'+r'\textbf{Prompt if stuck.} '+tex(u['hint'])+'\\par\\smallskip\n'+r'\textbf{Watch for.} '+tex(u['mis'])
        if codes(u): s+='\\par\\smallskip Full code: '+', '.join(r'\texttt{'+esc(fn)+r'} (page~\pageref{code-'+fn+'})' for fn in codes(u))+'.'
        s+='\n'+r'\end{minipage}\par\medskip{\color{lightink}\hrule height .4pt}\medskip'+'\n\n'
    s+=r'\topicflow{TRACE ANSWERS}{Completed diagrams and tables}'+'\n'
    for u in L['units']:
        d=u.get('answer_diagram') or u.get('diagram')
        if u['id'] in TABLES:
            d=dict(kind='table',head=TABLES[u['id']][0],rows=TABLE_ANSWERS[u['id']])
        if d:
            s+=r'\par\bigskip\begin{minipage}{\textwidth}\textbf{'+u['id']+' / '+tex(u['title'])+r'}\par'+diagram(d)+r'\end{minipage}'+'\n'
    if L['n']==1:
        s+=r'\Needspace{18\baselineskip}\textbf{Frog as a graph / L1-16 and L1-21}\par '+tex(FG.LINK)+r'\par\medskip\resizebox{\linewidth}{!}{'+FG.tikz(True)+r'}\par '+tex('Solid arrows recover 0, 2, 4, 5 at cost 30; dashed arrows are other legal jumps. '+FG.DIFFERENCE)+'\n'
    # Several listings per page; each listing stays on one page.
    s+=r'\topicflow{CODE ANSWERS}{Complete code}'+'\n'+'Every function used in class, in question order. Line numbers are the same as in the tutor book.\\par\\medskip\n'
    for u in L['units']:
        for fn in codes(u):
            code=precode(fn)
            block=r'{\color{teal}\textbf{'+u['id']+r'}}\quad\textbf{\texttt{'+esc(fn)+r'}}\label{code-'+fn+r'}\par'+numbered(code)
            extra=0
            if fn in RECURSIVE: block+=r'\textbf{Recursion depth.} '+tex(RECURSION_NOTE.split(': ',1)[1])+'\n\n'; extra+=3
            if u['run'] and len(codes(u))==1:
                block+=listing(u['run'])+r'\textbf{Expected output:} '+tex(example_output(u['run']))+'\n'; extra+=len(u['run'].splitlines())+3
            s+=r'\Needspace{'+str(len(code.splitlines())+extra+5)+r'\baselineskip}'+'\n'+block+r'\par\bigskip'+'\n'
    s+=r'\topicflow{EXERCISE CHECKS}{Expected notebook results}'+'\n'
    for ex in L['exercises']:
        s+=r'\Needspace{8\baselineskip}\textbf{'+ex['id']+' / '+tex(ex['function'])+'}\\par\n'
        s+='Use the complete '+r'\texttt{'+esc(ex['solution'])+r'} solution on page~\pageref{code-'+ex['solution']+'}.'
        if ex['function'] != ex['solution']:
            s+=' Rename the function to '+r'\texttt{'+esc(ex['function'])+'} to match the exercise.'
        else:
            s+=' The function name and parameters are the same in the notebook.'
        s+='\n'
        for args,want in ex['tests']: assert eval(call_text(ex['function'],args),NS(ex['function']))==want
        width=max(len(call_text(ex['function'],args)) for args,_ in ex['tests'])
        s+=listing('\n'.join(f"{call_text(ex['function'],args):<{width}}  # expected: {want}" for args,want in ex['tests']))
    s+=r'\end{document}'
    return s

def reference(L):
    s=r'\topic{KEEP BESIDE YOUR WORK}{The route and the rules}'+'\n'
    for title,body in GUIDES[L['n']]:
        s+=r'\textbf{'+tex(title)+r'}\par '+tex(body)+r'\par\medskip'+'\n'
    return s

def worksheet_answers(L):
    from answer_booklets import render
    return render(L)

def worksheet_printer_friendly(L):
    """Compact question-only handout; all supplied figures stay with their question."""
    s=bookhead(L,'worksheet')+cover(L,'worksheet-printer-friendly',colab=True)
    s+=r'\markboth{Questions}{}\raggedbottom\setlength{\parskip}{4pt}'+'\n'
    s+=r'{\heavy\fontsize{16}{20}\selectfont Lesson '+str(L['n'])+' / '+tex(L['subtitle'])+r'\par}\medskip'+'\n'
    last_topic=None
    for i,u in enumerate(L['units'],1):
        topic=part(L['n'],i)
        # Each whole question moves to the next page if it cannot fit, so its
        # referenced table or diagram can never be separated from its wording.
        s+=r'\par\noindent\begin{minipage}{\linewidth}'+'\n'
        if topic!=last_topic:
            s+=r'{\heavy\fontsize{12}{15}\selectfont '+tex(topic)+r'\par}\medskip'+'\n'
            last_topic=topic
        s+=r'\textbf{'+u['id']+(' / OPTIONAL EXTENSION' if u['extension'] else '')+' / '+tex(u['title'])+r'}\par\smallskip '+tex(u['q'])+r'\par'+'\n'
        if u.get('given'): s+=SP.code_tex(given_code(u).rstrip().splitlines(),tex)
        if u['id'] in IMPLEMENT: s+=SP.print_tex(u['id'],tex)
        d=u.get('diagram')
        if u['id'] in TABLES:
            head,rows=TABLES[u['id']]
            d=dict(kind='table',head=head,rows=rows)
        # Empty drawing boxes and ruled answer areas are omitted. Retain all
        # supplied information, including the blocked-grid input and call tree.
        if d and d['kind'] in ('table','tree'):
            visual=diagram(d,True).replace('fill=wash','fill=paper')
            if L['n']==1: visual=visual.replace(r'\medskip',r'\smallskip')
            s+=visual+'\n'
        if u['id']=='L1-21': s+=r'\par\smallskip\resizebox{\linewidth}{!}{'+FG.tikz()+r'}\par '+tex('Circles show stone indices; the height is below each circle. Each arrow is a legal jump, labelled with its cost. Mark the route returned by your program.')+'\n'
        s+=r'\end{minipage}\par\vspace{'+('2mm' if L['n']==1 else '4mm')+r'}'+'\n'
    return s+r'\end{document}'

SLIDESTART=r'\begin{frame}[plain,fragile]\begin{tikzpicture}[remember picture,overlay,x=1cm,y=1cm]\begin{scope}[shift={(current page.south west)}]'
SLIDEEND=r'\end{scope}\end{tikzpicture}\end{frame}'
def stxt(x,y,w,size,text,color='ink',name=None):
    return rf'\node{"("+name+")" if name else ""}[anchor=north west,inner sep=0pt,text width={w}cm,align=left,text={color},font=\fontsize{{{size}}}{{\dimexpr{size}pt*6/5\relax}}\selectfont] at ({x},{y}) {{{text}}};'+'\n'
def number(x=30,y=0.8):
    return stxt(x,y,1,11,r'\insertframenumber','quiet')
def foot(L,u,typ):
    return stxt(1.5,16.9,29,13,r'\heavy LESSON '+str(L['n'])+' / '+u['id']+' / '+typ,'quiet')+number()
def slide_table(u,answer):
    """The worksheet's table for this question: blank on the question slide, filled on the answer slide."""
    if u['id'] in TABLES:
        return TABLES[u['id']][0],(TABLE_ANSWERS[u['id']] if answer else TABLES[u['id']][1])
    d=(u.get('answer_diagram') or u['diagram']) if answer else u['diagram']
    if d and d['kind']=='table' and (answer or d.get('blank') or u['id'] in ('L1-15','L2-09')):
        a=u.get('answer_diagram')
        if answer and a: return (a['head'],a['rows']) if a['kind']=='table' else None
        return d['head'],(d['rows'] if answer else (d.get('blank') or d['rows']))
    return None
def slides(L):
    s=r"""\documentclass[aspectratio=169]{beamer}
\geometry{paperwidth=320mm,paperheight=180mm}
\input{common.tex}
\usepackage{colortbl}
\usetikzlibrary{fit}
\newsavebox{\codebox}
\setbeamercolor{normal text}{fg=ink,bg=paper}
\setbeamertemplate{navigation symbols}{}\setbeamertemplate{footline}{}\setbeamertemplate{headline}{}
\begin{document}
"""
    if L['n']==1:
        s=s.replace(r'\begin{document}',WARM.THEME+'\n'+r'\begin{document}',1)
    s+=SLIDESTART+'\n'+stxt(1.5,16.5,29,16,r'\heavy LESSON '+str(L['n']),'teal')+stxt(1.5,14.4,29,40 if L['n']==3 else 46,r'\heavy '+__import__('candies_style').TITLES[L['n']],'ink')+stxt(1.5,9.3,29,22,tex(L['title']),'quiet')
    s+=r'\node[anchor=south,inner sep=0] at (16,2.3) {\includegraphics[width=27cm,height=6cm,keepaspectratio]{assets/cover.png}};\node[anchor=west,inner sep=0] at (1.5,1) {\includegraphics[width=3.8cm]{assets/logo.png}};\node[anchor=east,inner sep=0] at (30.5,1) {\includegraphics[width=5.5cm]{assets/julians-pathfinder-monochrome.pdf}};'+'\n'+number(15.8,0.8)+SLIDEEND+'\n'
    # The title slide includes a direct link to the matching student notebook.
    link_node=stxt(18,16.5,12,14,colab_link(L),'ink')
    s=s.replace(SLIDEEND,link_node+SLIDEEND,1)
    # Slide 2: the main idea and what students will be able to do.
    s+=SLIDESTART+'\n'+stxt(1.5,16.9,29,13,r'\heavy LESSON '+str(L['n'])+' / TODAY','quiet')+number()
    s+=stxt(1.5,15.4,29,18,r'\heavy MAIN IDEA','quiet')+stxt(1.5,14.3,29,40,r'\heavy '+tex(L['title'])+'.')+stxt(1.5,11.9,28,24,tex(L['idea']),'ink','idea')
    s+=r'\node[anchor=north west,inner sep=0pt,text width=28cm,align=left,font=\fontsize{24}{30}\selectfont] at ([yshift=-9mm]idea.south west) {\textbf{You will be able to}\par\smallskip'+''.join(r'\hangindent=1.1em\hangafter=1\textbullet\ '+tex(x)+r'\par' for x in L['able'])+'};\n'+SLIDEEND+'\n'
    if L['n']==1: s+=RI.slides(SLIDESTART,SLIDEEND,stxt,number,ruled,tex)
    for u in L['units']:
        if u['id']=='L2-08': s+=DM.slides(SLIDESTART,SLIDEEND,stxt,number,tex,ruled)
        if u['id']=='L1-16': s+=FG.slides(SLIDESTART,SLIDEEND,stxt,number,tex)
        for answer in (False,True):
            s+=SLIDESTART+'\n'+foot(L,u,'ANSWER' if answer else ('QUESTION / OPTIONAL' if u['extension'] else 'QUESTION'))
            s+=stxt(1.5,15.4,29,34,r'\heavy '+tex(u['title']))
            table=slide_table(u,answer)
            d=(u.get('answer_diagram') or u['diagram']) if answer else u['diagram']
            if d and d['kind']=='table': d=None
            # Only show a diagram on questions if it does not reveal an answer.
            showd=bool(d and (answer or d['kind'] in ('tree','lastmove')))
            body=u['a'] if answer else u['q']
            custom=WARM.body(u,answer,tex,stxt) if L['n']==1 else None
            if custom is not None:
                s+=custom+SLIDEEND+'\n'
                continue
            illustrated=illustrated_body(u,answer,table,tex,stxt,ruled)
            if illustrated is not None:
                s+=illustrated+SLIDEEND+'\n'
                continue
            implement=u['id'] in IMPLEMENT and not answer
            s+=stxt(1.5,12.4,29,20 if implement else (22 if (showd or table or u.get('given')) else 25),tex(body),'ink','body')
            if u.get('given') and not answer:
                # Code supplied with the question: on the left, its table on the right.
                s+=SP.slide_code(given_code(u),tex,'body')
                if implement: s+=SP.slide_nodes(u['id'],tex,'given')
                if table: s+=r'\node[anchor=north west,inner sep=0,text width=14cm] at ([xshift=15cm,yshift=-8mm]body.south west) {'+ruled(table[0],table[1],tex,True)+'};\n'
            elif table:
                s+=r'\node(tab)[anchor=north west,inner sep=0,text width=29cm] at ([yshift=-8mm]body.south west) {'+ruled(table[0],table[1],tex,'compact' if implement else True)+'};\n'
                if implement: s+=SP.slide_nodes(u['id'],tex,'tab')
            elif implement:
                s+=SP.slide_nodes(u['id'],tex,'body')
            elif showd:
                if d['kind']=='gridroutes':
                    s+=r'\node[anchor=north west,inner sep=0] at (1.5,9.0) {\scalebox{1.4}{\begin{minipage}{16cm}'+diagram(d,not answer,True)+r'\end{minipage}}};'+'\n'
                else:
                    s+=r'\node[anchor=north west,inner sep=0,text width=28cm] at (1.5,6.5) {\resizebox{18cm}{!}{\begin{minipage}{14cm}'+diagram(d,not answer,True)+r'\end{minipage}}};'+'\n'
            elif u.get('given') and not answer: pass
            elif not answer:
                s+=stxt(1.5,4.0,28,22,'Think on your own first. Then compare your reasoning with a partner.','teal')
            else:
                s+=stxt(1.5,4.0,28,21,r'\textbf{Watch for:} '+tex(u['mis']),'teal')
            s+=SLIDEEND+'\n'
        if u['id']=='L1-21': s+=FG.slides(SLIDESTART,SLIDEEND,stxt,number,tex,True)
        # Complete programs follow the answer, split only between statements.
        for fn in codes(u):
            header=stxt(1.5,16.9,29,13,r'\heavy LESSON '+str(L['n'])+' / '+u['id']+' / ANSWER: PYTHON','quiet')+number()
            title=(fn+str(inspect.signature(getattr(P,fn)))) if L['n']==1 else fn.replace('_',' ')
            s+=code_slides(header,title,precode(fn),tex)
    # Closing summary: main idea, what we learned and an exit question.
    s+=SLIDESTART+'\n'+stxt(1.5,16.9,29,13,r'\heavy LESSON '+str(L['n'])+' / SUMMARY','quiet')+number()
    s+=stxt(1.5,15.4,29,18,r'\heavy MAIN IDEA','quiet')+stxt(1.5,14.3,29,36,r'\heavy '+tex(L['title'])+'.','ink','idea')
    s+=r'\node(learned)[anchor=north west,inner sep=0pt,text width=28.5cm,align=left,font=\fontsize{21}{26}\selectfont] at ([yshift=-7mm]idea.south west) {\textbf{What we learned}\par\smallskip'+''.join(r'\hangindent=1.1em\hangafter=1\textbullet\ '+tex(x)+r'\par' for x in L['learned'])+'};\n'
    s+=r'\node[anchor=north west,inner sep=4mm,fill=wash,text width=28cm,align=left,font=\fontsize{21}{26}\selectfont] at ([yshift=-7mm,xshift=-4mm]learned.south west) {\textbf{Exit question.} '+tex(L['exit'])+'};\n'+SLIDEEND+'\n'
    s+=r'\end{document}'
    return COH.apply(WARM.quiet_layout(s),stxt,tex,SLIDESTART,SLIDEEND,number) if L['n']==1 else s


def mdcell(s): return dict(cell_type='markdown',metadata={},source=s)
def codecell(s): return dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=s)
def notebook(L,teacher=False):
    intro=f"# Lesson {L['n']}: {L['title']}\n## {L['subtitle']}\n\nRun in Jupyter or Google Colab with Python 3. No packages or external input files are required. Shift+Enter runs a cell. Run the setup cell first. Predict each result before running code.\n\nExercise IDs match the worksheet and slides. Small recursive examples are for learning; use iteration for large inputs. Python stops recursion at about 1,000 nested calls by default, so recursive versions are for small inputs only.\n"
    if not teacher: intro+="\nWhere a question asks you to write a program, the cell below it is a stub: replace `return None` with your code, then run the check cell. Cells marked **Worked example** explain an idea; read them after you have tried the question.\n"
    cells=[mdcell(intro),codecell(setup_code(L))]
    cells.append(mdcell('## The route and the rules\n\n'+'\n\n'.join('### '+title+'\n'+body for title,body in GUIDES[L['n']])))
    exercises={e['id']:e for e in L['exercises']}
    if L['n']==1: cells.extend(RI.notebook_cells(mdcell, codecell, teacher))
    stubbed={}
    for u in L['units']:
        if u['id']=='L1-16': cells.append(FG.notebook_cell(mdcell))
        cells.append(mdcell(f"## {u['id']}: {u['title']}"+(' (optional extension)' if u['extension'] else '')+'\n\n'+u['q']))
        if u.get('given'):
            if not teacher and u['id'] in ('L1-01', 'L1-02'):
                cells.append(mdcell('**Code to trace:** run this definition cell first; it does not print the answer.'))
                cells.append(codecell(given_code(u)))
            else:
                cells.append(mdcell('```python\n'+given_code(u).rstrip()+'\n```'))
        if u['id'] in IMPLEMENT: cells.append(mdcell(SP.markdown(u['id'])))
        d=u['diagram']
        if u['id'] in TABLES: d=dict(kind='table',head=TABLES[u['id']][0],rows=TABLES[u['id']][1])
        if d and d['kind']=='table':
            rows=d.get('blank') or d['rows']
            md=lambda x: x.replace('*','\\*') if x.strip() else '&nbsp;'
            tabletext=' | '.join(md(x) for x in d['head'])+'\n'+' | '.join(['---']*len(d['head']))+'\n'+'\n'.join(' | '.join(md(x) for x in r) for r in rows)
            cells.append(mdcell(tabletext))
        elif d and d['kind']=='tree':
            cells.append(mdcell('The first three call levels (positive targets continue below this drawing):\n\n```text\nways(5)\n|-- ways(4)\n|   |-- ways(3)\n|   `-- ways(2)\n`-- ways(3)\n    |-- ways(2)\n    `-- ways(1)\n```'))
        cells.append(mdcell('**Your prediction / reasoning:**\n\nWrite your explanation here.'))
        if teacher and u['id']=='L1-21': cells.append(FG.notebook_cell(mdcell,True))
        if teacher:
            cells.append(mdcell('**Answer:** '+u['a']+'\n\n'+u['notes']))
            answered = u.get('answer_diagram') or u.get('diagram')
            if u['id'] in TABLES:
                answered = dict(kind='table', head=TABLES[u['id']][0], rows=TABLE_ANSWERS[u['id']])
            if answered and answered['kind'] == 'table':
                cells.append(mdcell('**Completed table:**\n\n' + ' | '.join(answered['head']) + '\n'
                    + ' | '.join(['---'] * len(answered['head'])) + '\n'
                    + '\n'.join(' | '.join(str(x).replace('*', '\\*') for x in row) for row in answered['rows'])))
        if u['id']=='L2-08': cells.append(mdcell(DM.markdown()))
        if not teacher and u['id'] in ('L1-01', 'L1-02'):
            fn, arg = ('countdown', 3) if u['id']=='L1-01' else ('sum_squares', 4)
            cells.append(codecell(RI.trace_check(fn, arg)))
            cells.append(mdcell(RI.reveal_table(TABLES[u['id']][0], TABLE_ANSWERS[u['id']])))
        ex=exercises.get(u['id'])
        if ex:
            if teacher:
                cells.append(codecell(inspect.getsource(getattr(P,ex['solution']))))
            elif ex['function'] in stubbed:
                # Never a second empty stub: it would replace the student's own function.
                cells.append(mdcell(f"**Use your `{ex['function']}` from {stubbed[ex['function']]}.** If you change it, run its cell again before the checks below."))
            else:
                cells.append(codecell(stub_source(ex['function'])))
                stubbed[ex['function']]=u['id']
            cells.append(codecell(check_cell(ex['function'],ex['tests'],'All exercise checks passed.')))
        elif teacher:
            for fn in codes(u):
                if fn in RECURSIVE: cells.append(mdcell('**'+RECURSION_NOTE.replace(': ',':** ',1)))
                cells.append(codecell(inspect.getsource(getattr(P,fn))))
            if u['run']: cells.append(codecell(u['run']))
        else:
            modes={fn:student_mode(L,u,fn) for fn in codes(u)}
            for fn,mode in modes.items():
                if mode=='skip': continue
                if fn in RECURSIVE and mode in ('stub','example'): cells.append(mdcell('**'+RECURSION_NOTE.replace(': ',':** ',1)))
                if mode=='stub':
                    cells.append(codecell(stub_source(fn)))
                    stubbed[fn]=u['id']
                    cells.append(codecell(check_cell(fn,stub_cases(fn))))
                elif mode=='hidden':
                    target=solves_exercise(L,fn)
                    cells.append(mdcell(f"**No code here.** Work this question by hand. You will write the iterative solution in {target['id']} as `{target['function']}`."))
                else:
                    cells.append(mdcell('**Worked example: read it after you have answered the question above.** It explains the idea and is not one of your exercises.'))
                    cells.append(codecell(inspect.getsource(getattr(P,fn))))
            if u['run'] and all(m=='example' for m in modes.values() if m!='skip'): cells.append(codecell(u['run']))
        if not teacher and codes(u) and not ex:
            shown=[m for m in modes.values() if m!='skip']
            if all(m=='hidden' for m in shown): lead='**Hint:** '
            elif 'stub' in shown: lead='**After completing the function:** Explain why each checked answer follows from the state and its earlier answers.\n\n'
            else: lead='**After running:** Explain why the output follows from the state and its earlier answers.\n\n'
            cells.append(mdcell(lead+u['hint']))
    image_data=base64.b64encode((ROOT/f'Lesson {L["n"]}'/'assets/cover.png').read_bytes()).decode()
    cells[0]['source'] += '\n\n![Lesson illustration](attachment:cover.png)'
    cells[0]['attachments']={'cover.png':{'image/png':image_data}}
    cells.append(mdcell('## Original problem sources\n'+'\n'.join(f'- [{name}]({url})' if url.startswith('http') else '- '+name+': '+url for name,url in L['sources'])))
    return dict(nbformat=4,nbformat_minor=5,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3.11')),cells=[dict(c,id=f'cell-{i:03}') for i,c in enumerate(cells)])


def build(only=None):
    from compile_all import source_path
    for L in C.LESSONS:
        if only is not None and L['n'] not in only: continue
        dest=ROOT/f'Lesson {L["n"]}'
        (dest/'fonts').mkdir(exist_ok=True);(dest/'assets').mkdir(exist_ok=True);(dest/'programs').mkdir(exist_ok=True)
        for name in ['AvenirNext.ttc','JetBrainsMono-Regular.ttf']:
            if (FONT/name).resolve() != (dest/'fonts'/name).resolve():
                shutil.copy2(FONT/name,dest/'fonts'/name)
        # Each lesson keeps its own cover asset; regeneration preserves it.
        style_assets(dest)
        (dest/'common.tex').write_text(COMMON)
        for kind,fn in [('tutorial',tutorial),('teacher',teacher),('worksheet-printer-friendly',worksheet_printer_friendly),('worksheet_answers',worksheet_answers),('slides',slides)]:
            text=fn(L)
            if kind=='slides': text=text.replace(r'\end{frame}', '\n'+r'\end{frame}'+'\n')
            source_path(L['n'],kind).write_text(text)
        for name,teacherflag in [('lesson',False),('teacher-notebook',True)]: (dest/f'{name}.ipynb').write_text(json.dumps(notebook(L,teacherflag),indent=1))
        functions=lesson_functions(L)
        allcode=(constants_for(functions)+'\n' if constants_for(functions) else '')+'\n'.join(inspect.getsource(getattr(P,fn)) for fn in functions)
        (dest/'solutions.py').write_text(allcode)
        for fn in FUNCTIONS[L['n']]: (dest/'programs'/f'{fn}.py').write_text(precode(fn)+'\n'+WRAPPERS[fn])
        (dest/'README.txt').write_text(f'''LESSON {L['n']} - {L['title']}\n{L['subtitle']}\n\nFOR THE TEACHER\n../Teacher/teacher-book.pdf: one detailed preparation book covering all five lessons.\n../Teacher/teacher-class-notes.pdf: all five lesson plans, classroom questions, hints, answers and code.\nworksheet_answers.pdf: questions in worksheet order, worked answers, completed tables and full code.\nslides.pdf: questions immediately followed by answers; code continuations follow the answer.\nteacher-notebook.ipynb: worked answers and completed exercise functions.\nsolutions.py: all complete classroom functions in one file. Recursive versions are for small inputs: Python stops recursion at about 1,000 nested calls.
solution.py: separate final iterative functions using the same test runner as starter.py.\n\nGIVE STUDENTS\nstarter.py: function skeletons; run python3 starter.py for small and edge tests.\nrunner.py and test-cases/: loading, comparisons and small/medium/large datasets.\nPRACTICE.txt: all commands, input formats and sizes.\nworksheet-printer-friendly.pdf: the student worksheet: illustrated cover, compact question pages and a Colab link.\nlesson.ipynb: questions, labelled worked examples and stub cells to complete; Python standard library only.\nstudent-pack.zip contains the worksheet, notebook, starter.py, runner.py, test-cases/ and PRACTICE.txt; it excludes solutions.\n\nOPEN THE NOTEBOOK\nOpen lesson.ipynb in Jupyter, or upload it to Google Colab. Select Python 3.\nRun the setup cell, then proceed top to bottom. Shift+Enter executes a cell.\nExercise functions initially return None; checks say 'Not implemented yet' until completed.\nDo not share teacher-notebook.ipynb or the complete folder as the student handout.\n\nEDIT / REBUILD\nClassroom PDFs have matching .tex files with common.tex, fonts and assets. The two teacher books and their sources are in ../Teacher/.\nCourse source/compile_all.py compiles all PDFs into Course source/build/ (outside this folder),\nand Course source/publish.py copies the checked PDFs here.\nTo compile one file by hand, run XeLaTeX twice: xelatex slides.tex\nmain.tex opens slides.tex by default in the built-in editor.\nCourse source/build_course.py regenerates all lesson sources from the shared content.\nPrograms in programs/ include complete judge input/output adapters.\n\nPALETTE\nMatched to Distributing Candies: white #FFFFFF; charcoal #252525; muted grey #666666; code paper #F6F6F4. Avenir Next and JetBrains Mono; original partner logos.\n''')
        (dest/'main.tex').write_text(r'\input{slides.tex}'+'\n')
        print(f"Lesson {L['n']}: {len(L['units'])} question/answer pairs; {len(functions)} complete functions")
if __name__=='__main__':
    build()
    from make_practice import build as build_practice
    build_practice()
    from build_teacher_books import generate as generate_teacher_books
    generate_teacher_books()
