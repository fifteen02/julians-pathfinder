"""Build two course-wide teacher volumes from the existing lesson generators."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import re
import shutil
import subprocess
from content import LESSONS
import build_course as B
import build_books as BK

ROOT=Path(__file__).resolve().parent.parent
HERE=ROOT/'Course source'
DEST=ROOT/'Teacher'
OUT=HERE/'build'/'Teacher'
NAMES=('teacher-book','teacher-class-notes')
COURSE_TITLE='Dynamic Programming: From Recursion to Efficient Solutions'

def cover(name):
    detailed=name=='teacher-book'
    volume='Teacher Book' if detailed else 'Class Notes'
    lead=(r'Prepare the reasoning, work through the examples,\\and understand the complete solutions.' if detailed else
          r'Plan the session, ask the questions,\\and work through the answers together.')
    return r'''\thispagestyle{empty}\null
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-24mm]current page.north west) {\heavy\fontsize{43}{47}\selectfont\raggedright Dynamic\\Programming};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-68mm]current page.north west) {\fontsize{19}{25}\selectfont\raggedright From Recursion to Efficient Solutions};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-94mm]current page.north west) {\heavy\fontsize{15}{19}\selectfont '''+volume+r'''\quad {\normalfont\color{quiet}Lessons 1–5}};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-107mm]current page.north west) {\fontsize{12}{16}\selectfont\raggedright '''+lead+r'''};
\node[anchor=center,inner sep=0] at ([xshift=105mm,yshift=-166mm]current page.north west) {\includegraphics[width=174mm,height=88mm,keepaspectratio]{assets/cover.png}};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-226mm]current page.north west) {\fontsize{12}{16}\selectfont Staircase and Frog · Dice and Grid Paths\\Tower and Array Description · Fruit Feast\\Hoof, Paper, Scissors};
\node[anchor=west,inner sep=0] at ([xshift=18mm,yshift=-269mm]current page.north west) {\includegraphics[width=43mm]{assets/logo.png}};
\node[anchor=east,inner sep=0] at ([xshift=192mm,yshift=-269mm]current page.north west) {\includegraphics[width=62mm]{assets/julians-pathfinder-monochrome.pdf}};
\end{tikzpicture}\clearpage
'''

def contents(name):
    detailed=name=='teacher-book'
    s=r'\markboth{Contents}{}\pdfbookmark[0]{Contents}{contents}\noindent\makebox[\linewidth][l]{\begin{minipage}{176mm}{\heavy\fontsize{28}{33}\selectfont Contents\par}\vspace{5mm}'+'\n'
    intro=('Read the relevant lesson before class. Each lesson develops the ideas through worked examples, diagrams, complete programs and explanations of their running time. Margin notes identify the matching classroom questions.' if detailed else
           'Keep this book open during class. Each lesson contains its timetable, questions, hints, worked answers, completed traces and full code. Give students time to attempt each question before revealing its answer.')
    s+=r'\begin{minipage}{140mm}\raggedright '+B.tex(intro)+r'\end{minipage}\par\vspace{7mm}'+'\n'
    for L in LESSONS:
        n=L['n']
        s+=(r'\noindent\begin{minipage}[t][29mm][t]{176mm}\vspace{0pt}'
            r'{\color{lightink}\hrule height .35pt}\vspace{5mm}'
            r'\begin{minipage}[t]{18mm}\vspace{0pt}{\heavy\fontsize{26}{29}\selectfont '+str(n)+r'}\end{minipage}'
            r'\begin{minipage}[t]{140mm}\vspace{0pt}{\heavy\fontsize{14}{18}\selectfont\hyperref[lesson-'+str(n)+']{'+B.tex(L['subtitle'])+r'}\par}\vspace{2mm}{\color{quiet}'+B.tex(L['title'])+r'.}\end{minipage}'
            r'\begin{minipage}[t]{18mm}\vspace{0pt}\raggedleft{\heavy\fontsize{14}{18}\selectfont\pageref{lesson-'+str(n)+r'}}\end{minipage}\end{minipage}\par'+'\n')
    s+=r'\vspace{5mm}\begin{minipage}{140mm}\raggedright\textbf{Using the two books}\par '+B.tex('Teacher Book is for preparation. Teacher Class Notes is for teaching. Question IDs such as L1-04 match the worksheets, slides and notebooks. Each lesson folder holds the classroom materials and practice files.')+r'\end{minipage}\end{minipage}}'+'\n'
    return s

def lesson_title(L):
    """One opening hierarchy for both volumes; the lesson number is navigation."""
    return (r'\noindent\makebox[\linewidth][l]{\begin{minipage}{176mm}{\heavy\fontsize{23}{28}\selectfont\raggedright Lesson '
            +str(L['n'])+r'\par}\vspace{2mm}{\heavy\fontsize{19}{24}\selectfont\raggedright '
            +B.tex(L['subtitle'])+r'\par}\end{minipage}}\par\vspace{5mm}'+'\n')

def preamble(name):
    if name=='teacher-book':
        pre=BK.PREAMBLE
        pre=pre.replace('Lesson @NUMBER@ · @SUBTITLE@',r'\lessonheading')
        pre=pre.replace(r'LESSON @NUMBER@\quad /\quad @SUBTITLE@',r'\lessonheading')
        pre=pre.replace(r'PART \thechapter',r'SECTION \thechapter')
        extra=r'\renewcommand{\thechapter}{\lessonnumber.\arabic{chapter}}\renewcommand{\theHchapter}{\lessonnumber.\arabic{chapter}}'
    else:
        pre=B.bookhead(LESSONS[0],'teacher')
        pre=pre.replace('Lesson 1 · Staircase and Frog',r'\lessonheading')
        pre=pre.replace('LESSON 1 / Staircase and Frog',r'\lessonheading')
        pre=pre.replace(r'Teacher · ', '')
        extra=''
    title='Teacher Book' if name=='teacher-book' else 'Teacher Class Notes'
    extra+='\n'+r'\newcommand{\lessonnumber}{0}\newcommand{\lessonheading}{'+title+r'}\hypersetup{pdftitle={'+COURSE_TITLE+' - '+title+r'},pdfauthor={fifteen02},bookmarksopen=true}'+'\n'
    # Distinguish the volumes at a glance without repeating the long header.
    pre=pre.replace(r'\fancyfoot[L]{\fontsize{8}{10}\selectfont\color{quiet}\lessonheading}',r'\fancyfoot[L]{\fontsize{8}{10}\selectfont\color{quiet}'+title+r'\ifnum\lessonnumber>0\relax\quad /\quad Lesson \lessonnumber\fi}')
    extra+=r'\fancyfoot[R]{\heavy\fontsize{10}{12}\selectfont\color{ink}\thepage}'+'\n'
    extra+=r'\widowpenalty=10000\clubpenalty=10000\displaywidowpenalty=10000'+'\n'
    return pre.replace(r'\begin{document}',extra+r'\begin{document}')

def lesson_body(L,name):
    n=L['n']
    if name=='teacher-book':
        source=BK.render(L)
        begin=source.index(r'\chapter*{The route through this book}')
        body=source[begin:source.rindex(r'\end{document}')]
        body=body.replace(r'\clearpage\tableofcontents\clearpage','')
        body=body.replace(r'\appendix','')
        old=r'\chapter*{The route through this book}\addcontentsline{toc}{chapter}{The route through this book}\markboth{The route through this book}{}'
        body=body.replace(old,lesson_title(L)+r'\markboth{The lesson route}{}',1)
        counters=r'\setcounter{chapter}{0}\setcounter{section}{0}'
    else:
        source=B.teacher(L)
        body=source.split(B.cover(L,'teacher',colab=True),1)[1].rsplit(r'\end{document}',1)[0]
        body=body.replace(r'\topic{BEFORE CLASS}',r'\topicflow{BEFORE CLASS}',1)
        body=lesson_title(L)+B.colab_link(L)+r'\par'+'\n'+body
        # Minutes and IDs are short; reserve the wide column for activities.
        oldcols=r'\begin{tabularx}{\linewidth}{'+r'>{\raggedright\arraybackslash}X'*3+r'}\toprule\textbf{Minutes}'
        newcols=r'\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{18mm}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}p{38mm}}\toprule\textbf{Minutes}'
        body=body.replace(oldcols,newcols,1)
        counters=''
    body=body.replace('The route through this book','The route through this lesson')
    body=body.replace('Read this book before the lesson.', 'Read this lesson before class.')
    body=body.replace('the separate teacher guide', 'Teacher Class Notes').replace('The separate teacher guide','Teacher Class Notes')
    body=body.replace('Use the teacher guide','Use Teacher Class Notes')
    if name=='teacher-book':
        # Original chapters use local section numbers; the combined volume prefixes the lesson.
        body=re.sub(r'\bsection (\d+\.\d+)(?![\d.])',lambda m:'section '+str(n)+'.'+m[1],body)
    # All references within a lesson remain local even when code names repeat.
    body=re.sub(r'\\(label|pageref|ref|autoref)\{([^}]+)\}',lambda m:'\\'+m[1]+'{L'+str(n)+'-'+m[2]+'}',body)
    prefix=(r'\clearpage\renewcommand{\lessonnumber}{'+str(n)+r'}\renewcommand{\lessonheading}{Lesson '+str(n)+' · '+B.tex(L['subtitle'])+'}'+counters+
            r'\phantomsection\label{lesson-'+str(n)+r'}\pdfbookmark[-1]{Lesson '+str(n)+': '+B.tex(L['subtitle'])+'}{lesson-'+str(n)+'-bookmark}\n')
    return prefix+body

def generate():
    DEST.mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'Lesson 1/fonts',DEST/'fonts',dirs_exist_ok=True)
    (DEST/'assets').mkdir(exist_ok=True)
    for name in ('cover.png','logo.png','julians-pathfinder-monochrome.pdf'):
        shutil.copy2(ROOT/'Lesson 1/assets'/name,DEST/'assets'/name)
    (DEST/'common.tex').write_text(B.COMMON)
    for name in NAMES:
        text=preamble(name)+cover(name)+contents(name)
        for L in LESSONS:text+=lesson_body(L,name)
        (DEST/f'{name}.tex').write_text(text+r'\end{document}'+'\n')
    (DEST/'main.tex').write_text(r'\input{teacher-book.tex}'+'\n')
    (DEST/'README.txt').write_text(COURSE_TITLE+'\nTEACHER MATERIALS - LESSONS 1-5\n\nTeacher Book (teacher-book.pdf): detailed preparation, reasoning, worked examples, diagrams and complete implementations.\nTeacher Class Notes (teacher-class-notes.pdf): classroom timings, questions, hints, solutions, traces and complete code.\n\nBoth volumes have linked contents and continuous page numbering. Question IDs match the lesson worksheets, slides and notebooks.\n\nEdit the generators in Course source/, then run python3 -B build_teacher_books.py and python3 -B publish.py there. Do not hand-edit generated TeX.\nTo compile a saved volume directly, run XeLaTeX three times from this folder on its .tex file. main.tex selects Teacher Book.\n')

def compile_volume(name):
    for _ in range(3):
        run=subprocess.run(['/Library/TeX/texbin/xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(OUT),name+'.tex'],cwd=DEST,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (OUT/f'{name}-compile.txt').write_text(run.stdout)
        if run.returncode:return dict(name=name,ok=False,tail=run.stdout[-2500:])
    warnings=[line for line in (OUT/f'{name}.log').read_text().splitlines() if any(x in line for x in ('Overfull','Missing character','undefined','multiply defined'))]
    return dict(name=name,ok=not warnings,warnings=warnings,source_sha256=hashlib.sha256((DEST/f'{name}.tex').read_bytes()).hexdigest())

def build():
    generate()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(compile_volume,NAMES))
    (HERE/'teacher-books-compile-report.json').write_text(json.dumps(results,indent=2))
    for r in results:print(r)
    if not all(x['ok'] for x in results):raise RuntimeError('Teacher books did not compile cleanly')
    return results

if __name__=='__main__':build()
