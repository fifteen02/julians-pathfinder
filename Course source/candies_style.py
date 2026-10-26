"""Shared typography and page furniture, matched to the Distributing Candies guide."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent.parent
REFERENCE=ROOT/'Future lesson - Distributing Candies/tutorial-notes'
COMMON=r'''\usepackage{fontspec}
\setmainfont[Path=fonts/,FontIndex=7,BoldFont=AvenirNext.ttc,BoldFeatures={FontIndex=2},ItalicFont=AvenirNext.ttc,ItalicFeatures={FontIndex=4},BoldItalicFont=AvenirNext.ttc,BoldItalicFeatures={FontIndex=3}]{AvenirNext.ttc}
\setsansfont[Path=fonts/,FontIndex=7,BoldFont=AvenirNext.ttc,BoldFeatures={FontIndex=2},ItalicFont=AvenirNext.ttc,ItalicFeatures={FontIndex=4},BoldItalicFont=AvenirNext.ttc,BoldItalicFeatures={FontIndex=3}]{AvenirNext.ttc}
\newfontfamily\heavy[Path=fonts/,FontIndex=2]{AvenirNext.ttc}
\setmonofont[Path=fonts/,BoldFont=JetBrainsMono-Bold.ttf,ItalicFont=JetBrainsMono-Italic.ttf,Contextuals=NoAlternate,Ligatures=NoCommon]{JetBrainsMono-Regular.ttf}
\usepackage{xcolor,graphicx,tikz,booktabs,tabularx,listings,amsmath}
\usetikzlibrary{arrows.meta,positioning}
\definecolor{paper}{HTML}{FFFFFF}
\definecolor{ink}{HTML}{252525}
\definecolor{teal}{HTML}{252525}
\definecolor{orange}{HTML}{777777}
\definecolor{wash}{HTML}{EAEAEA}
\definecolor{quiet}{HTML}{666666}
\definecolor{lightink}{HTML}{D0D0D0}
\definecolor{codepaper}{HTML}{F6F6F4}
\lstset{language=Python,basicstyle=\ttfamily\fontsize{9.5}{13}\selectfont\color{ink},keywordstyle=\bfseries\color{ink},commentstyle=\itshape\color{quiet},stringstyle=\color{ink},showstringspaces=false,columns=fullflexible,keepspaces=true,breaklines=true,breakatwhitespace=true,numbers=none,upquote=true,aboveskip=8pt,belowskip=6pt}
\hyphenpenalty=4000
\emergencystretch=3em
% The same two-line navigation and fine rule as the reference, without a candy motif.
\newcommand{\guideheader}[2]{\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0,text width=176mm] at ([xshift=16mm,yshift=-7mm]current page.north west) {\fontsize{8.5}{10}\selectfont\color{quiet}#1};
\node[anchor=north west,inner sep=0,text width=176mm] at ([xshift=16mm,yshift=-11.5mm]current page.north west) {\heavy\fontsize{10}{12}\selectfont\color{ink}#2};
\draw[lightink,line width=.4pt] ([xshift=16mm,yshift=-17mm]current page.north west)--([xshift=192mm,yshift=-17mm]current page.north west);
\end{tikzpicture}}
'''

def assets(dest):
    # Prefer bundled assets so the complete course ZIP remains self-contained.
    for subdir, names, original in [
        ('assets', ['logo.png', 'julians-pathfinder-monochrome.pdf'], 'images'),
        ('fonts', ['JetBrainsMono-Bold.ttf', 'JetBrainsMono-Italic.ttf'], 'fonts')]:
        for name in names:
            source = ROOT/'Lesson 1'/subdir/name
            if not source.exists():
                source = REFERENCE/original/name
            target = dest/subdir/name
            if source.resolve() != target.resolve():
                shutil.copy2(source, target)

TITLES={1:r'Staircase\\and Frog',2:r'Dice and\\Grid Paths',3:r'Mortal Kombat Tower\\and Array Description',4:r'Fruit\\Feast',5:r'Hoof, Paper,\\Scissors'}

def colab_url(n):
    return f'https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%20{n}/lesson.ipynb'

def colab_link(L):
    return r'\href{'+colab_url(L['n']).replace('%',r'\%')+r'}{\underline{Open this lesson in Google Colab}}'

def cover(L,kind,colab=False):
    printer=kind=='worksheet-printer-friendly'
    if printer: kind='worksheet'
    n=L['n']; title=TITLES[n]; size=33 if n==3 else 43
    sub={'tutorial':'A complete guided explanation.','teacher':'Teaching prompts and worked answers.','worksheet':'Questions, traces and space to think.'}[kind]
    lead={'tutorial':r'Follow the examples and the reasoning,\\then run the complete implementations.', 'teacher':r'Ask a question, give students time to think,\\then work through the answer together.', 'worksheet':r'Make a prediction. Show your working.\\Explain why your answer follows.'}[kind]
    label={'tutorial':'TUTOR BOOK','teacher':'TEACHER GUIDE','worksheet':'STUDENT WORKSHEET'}[kind]
    if printer:
        sub='Questions, diagrams and tables.'
        lead=r'Try each question on paper or in the notebook.\\Use the same question IDs to check your answers.'
        label='PRINTER-FRIENDLY WORKSHEET'
    closing=r'Understand what each step establishes\\and why it leads to the next.'
    link=(r'\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-244mm]current page.north west) {\fontsize{11}{14}\selectfont '+colab_link(L)+'};\n') if colab else ''
    return r'''\thispagestyle{empty}\pagecolor{white}\null
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-22mm]current page.north west)
{\heavy\fontsize{9}{12}\selectfont ALGORITHMS\quad /\quad LESSON '''+f'{n:02d}'+r'''\quad /\quad '''+label+r'''};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-39mm]current page.north west)
{\heavy\fontsize{'''+str(size)+'}{'+str(size+4)+r'''}\selectfont\raggedright\spaceskip=.25em '''+title+r'''\par};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-80mm]current page.north west)
{\fontsize{19}{25}\selectfont '''+sub+r'''};
\node[anchor=north west,inner sep=0,text width=150mm] at ([xshift=18mm,yshift=-97mm]current page.north west)
{\fontsize{12}{16}\selectfont '''+lead+r'''};
\node[anchor=center,inner sep=0] at ([xshift=105mm,yshift=-167mm]current page.north west)
{\includegraphics[width=174mm,height=94mm,keepaspectratio]{assets/cover.png}};
\node[anchor=north west,inner sep=0,text width=174mm] at ([xshift=18mm,yshift=-224mm]current page.north west)
{\fontsize{12}{16}\selectfont '''+closing+r'''};
\node[anchor=west,inner sep=0] at ([xshift=18mm,yshift=-269mm]current page.north west)
{\includegraphics[width=43mm]{assets/logo.png}};
\node[anchor=east,inner sep=0] at ([xshift=192mm,yshift=-269mm]current page.north west)
{\includegraphics[width=62mm]{assets/julians-pathfinder-monochrome.pdf}};
'''+link+r'''\end{tikzpicture}\clearpage
'''
