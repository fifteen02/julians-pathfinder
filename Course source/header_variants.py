"""Three isolated header studies; does not alter the classroom deck."""
from pathlib import Path
import re
import subprocess
import build_course as B
import content as C

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'build'/'header-variants'
OUT.mkdir(parents=True,exist_ok=True)
source=B.slides(C.LESSONS[0])
preamble=source.split(r'\begin{document}',1)[0]
preamble=re.sub(r'\\setbeamertemplate\{background\}.*?\\end\{tikzpicture\}\}',r'\\setbeamertemplate{background}{}',preamble,flags=re.S)
frames=re.findall(r'\\begin\{frame\}.*?\\end\{frame\}',source,re.S)
original=frames[4]
# Preserve the objective, code, explanation and stack exactly as in the lesson.
body=original[original.index(r'\node[anchor=north west,inner sep=0pt,text width=29cm,align=left,text=quiet,font=\fontsize{21}') : original.index(r'\end{scope}\end{tikzpicture}')]
variants=[]
for letter,name in [('A','Quiet title'),('B','Title accent'),('C','Warm panel')]:
    head=B.SLIDESTART+'\n'
    if letter=='C':
        head+=r'\fill[codepaper] (0,13.9) rectangle (32,18);'+'\n'
        head+=B.stxt(23.8,16.1,6.7,15,r'Lesson 1\par Recursion','callink')
    if letter=='B':
        # A small typographic punctuation mark beside the heading, never a progress bar.
        head+=r'\fill[callink] (1.5,15.25) rectangle (1.7,16.45);'+'\n'
    head+=B.stxt(2.3 if letter=='B' else 1.5,16.5,20.5,40,r'\heavy The call stack','callink' if letter=='B' else 'ink')
    if letter!='C':
        head+=B.stxt(1.5,0.8,18,12,'Lesson 1 / Recursion','quiet')
    head+=B.stxt(24,0.8,7,12,f'{letter} / {name}','quiet')
    variants.append(head+body+B.SLIDEEND+'\n')
tex=preamble+r'\begin{document}'+'\n'+''.join(variants)+r'\end{document}'
tex=tex.replace(r'\end{frame}','\n'+r'\end{frame}'+'\n')
path=OUT/'header-variants.tex';path.write_text(tex)
for _ in range(2):
    r=subprocess.run(['/Library/TeX/texbin/xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(OUT),str(path)],cwd=ROOT/'Lesson 1',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (OUT/'compile.txt').write_text(r.stdout)
    if r.returncode: raise RuntimeError(r.stdout[-2500:])
warnings=[s for s in (OUT/'header-variants.log').read_text().splitlines() if any(k in s for k in ['Overfull','Missing character','undefined'])]
assert not warnings,warnings
print('Compiled three header variants without warnings.')
# Keep previews outside the classroom lesson pack.
import shutil
preview=ROOT/'Slide preview'
preview.mkdir(exist_ok=True)
shutil.copy2(OUT/'header-variants.pdf',preview/'header-variants.pdf')
