"""Warm slide-only colours and editable, computed recursion diagrams for Lesson 1."""
import programs as P

THEME = r'''
\definecolor{ink}{HTML}{302A26}
\definecolor{quiet}{HTML}{6D5D52}
\definecolor{teal}{HTML}{35634B}
\definecolor{orange}{HTML}{AC4A32}
\definecolor{wash}{HTML}{F9EBD8}
\definecolor{lightink}{HTML}{D8C5B7}
\definecolor{codepaper}{HTML}{FFF4E7}
\definecolor{callink}{HTML}{AC4A32}
\definecolor{callwash}{HTML}{FCE4D9}
\definecolor{waitink}{HTML}{875A16}
\definecolor{waitwash}{HTML}{FFF0C2}
\definecolor{returnink}{HTML}{35634B}
\definecolor{returnwash}{HTML}{E1EFE3}
\lstset{keywordstyle=\bfseries\color{callink},stringstyle=\color{returnink},commentstyle=\itshape\color{quiet}}
\setbeamertemplate{background}{}
'''


def box(key,x,y,label,tex,style='call',width=5.0,size=19):
    return (rf'\node({key})[draw={style}ink,line width=1.3pt,fill={style}wash,rounded corners=3mm,'
            rf'minimum width={width}cm,minimum height=1.15cm,align=center,font=\fontsize{{{size}}}{{{size+4}}}\selectfont]'
            rf' at ({x},{y}) {{{tex(label)}}};'+'\n')


def edge(a,b,label='',tex=str,style='call'):
    note=(r'node[midway,fill=white,inner sep=2pt,font=\fontsize{15}{18}\selectfont,text='+style+'ink]{'+tex(label)+'}') if label else ''
    return rf'\draw[-{{Stealth[length=3mm]}},line width=1.5pt,{style}ink] ({a}.south)--{note}({b}.north);'+'\n'


def body(u,answer,tex,stxt):
    ident=u['id']
    if ident not in ('L1-08','L1-09','L1-16') or (not answer and ident!='L1-09'):
        return None
    s=stxt(1.5,12.4,29,20,tex(u['a'] if answer else u['q']),'ink','body')
    if ident=='L1-08':
        s+=stxt(1.5,8.8,9,17,tex('Data: n = 3. Every box is a call to stairs_slow(n).'),'quiet')
        nodes=[('a',16,8.3,3),('b',10,6.2,2),('c',25,6.2,1),('d',6,4.2,1),('e',14,4.2,0),('f',22,4.2,0),('g',28,4.2,-1),('h',3,1.9,0),('i',9,1.9,-1)]
        for key,x,y,n in nodes:
            style='return' if n<=0 else 'wait' if n==1 else 'call'
            label=f'n = {n} / returns {P.stairs_slow(n)}'
            s+=box(key,x,y,label,tex,style,4.8,16)
        for a,b in [('a','b'),('a','c'),('b','d'),('b','e'),('c','f'),('c','g'),('d','h'),('d','i')]:s+=edge(a,b)
        s+=stxt(14.5,2.5,15,18,r'\textcolor{returnink}{\textbf{Green: base cases.}}\par\textcolor{waitink}{\textbf{Amber: n = 1 is solved twice.}}')
    else:
        frog=ident=='L1-16'
        ns=[5,4,3,3,2,2,1]
        positions=[(16,8.3),(9,5.9),(24,5.9),(3.8,3.5),(12,3.5),(21,3.5),(28,3.5)]
        keys=list('abcdefg')
        heights=[20,50,30,40,10,10]
        if frog:
            s+=stxt(1.5,9.6,29,18,tex('Data: heights = [20, 50, 30, 40, 10, 10]. Arrows label the final jump cost.'),'quiet')
        else:
            s+=stxt(1.5,8.8,9,17,tex('First three call levels. Positive inputs continue below the drawing.'),'quiet')
        for key,(x,y),n in zip(keys,positions,ns):
            style='call'
            if answer and n==3:style='wait'
            elif answer and n==2:style='wait'
            label=f'cost({n}) = {P.frog_table(heights[:n+1])}' if frog else f'ways({n})'
            s+=box(key,x,y,label,tex,style,5.1,18)
        for a,b in [('a','b'),('a','c'),('b','d'),('b','e'),('c','f'),('c','g')]:
            label=''
            if frog:
                na,nb=ns[keys.index(a)],ns[keys.index(b)]
                label='+'+str(abs(heights[na]-heights[nb]))
            s+=edge(a,b,label,tex)
        if answer:
            noun='cost' if frog else 'ways'
            if frog:
                c4,c3=P.frog_table(heights[:5]),P.frog_table(heights[:4])
                j4,j3=abs(heights[5]-heights[4]),abs(heights[5]-heights[3])
                caption=f'At stone 5: min({c4} + {j4}, {c3} + {j3}) = {min(c4+j4,c3+j3)}. Only the first three call levels are shown.'
            else:
                caption='Amber marks repeated inputs: ways(3) and ways(2). A cache saves each answer once.'
            s+=stxt(1.5,1.7,29,19,tex(caption),'quiet')
        else:
            s+=stxt(1.5,1.7,29,19,'Circle calls with the same input. The answer slide marks the matching pairs.','quiet')
    return s


def quiet_layout(source):
    """Apply the selected A layout to Lesson 1; content stays in place."""
    import re
    output=[]
    for line in source.splitlines(keepends=True):
        if r'\node' in line:
            if 'at (1.5,16.9)' in line:
                line=line.replace('at (1.5,16.9)', 'at (1.5,0.8)')
                line=line.replace(r'\fontsize{13}{\dimexpr13pt*6/5\relax}', r'\fontsize{12}{\dimexpr12pt*6/5\relax}')
                line=line.replace(r'\heavy LESSON', 'Lesson')
                line=re.sub(r'text=(?:callink|returnink)', 'text=quiet', line)
            elif 'at (1.5,15.4)' in line and r'\heavy MAIN IDEA' in line:
                continue
            elif 'at (1.5,15.4)' in line:
                line=line.replace('at (1.5,15.4)', 'at (1.5,16.5)')
                line=line.replace(r'\fontsize{34}{\dimexpr34pt*6/5\relax}', r'\fontsize{40}{\dimexpr40pt*6/5\relax}')
                line=line.replace(r'\fontsize{34}{40.8}', r'\fontsize{40}{48}')
            elif 'at (1.5,14.3)' in line:
                line=line.replace('at (1.5,14.3)', 'at (1.5,16.5)')
            elif 'at (1.5,16.5)' in line and r'\heavy LESSON 1' in line:
                line=line.replace('at (1.5,16.5)', 'at (1.5,10.8)')
                line=line.replace(r'\heavy LESSON 1', 'Lesson 1')
            elif 'at (1.5,14.4)' in line:
                line=line.replace('at (1.5,14.4)', 'at (1.5,16.5)')
        output.append(line)
    return ''.join(output)
