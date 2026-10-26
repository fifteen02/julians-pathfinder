"""Rebuild visual sources without replacing notebooks, code or datasets."""
from content import LESSONS
from compile_all import source_path
import build_course as b
for L in LESSONS:
    d=b.ROOT/f'Lesson {L["n"]}'
    b.style_assets(d)
    (d/'common.tex').write_text(b.COMMON)
    for k,f in [('tutorial',b.tutorial),('teacher',b.teacher),('worksheet-printer-friendly',b.worksheet_printer_friendly),('slides',b.slides)]:
        text=f(L)
        if k=='slides': text=text.replace(r'\end{frame}', '\n'+r'\end{frame}'+'\n')
        source_path(L['n'],k).write_text(text)
    readme=d/'README.txt'
    readme.write_text(readme.read_text().replace('Cream #F5F0E6; charcoal #242820; teal #176B68; burnt orange #D66A43.','Matched to Distributing Candies: white #FFFFFF; charcoal #252525; muted grey #666666; code paper #F6F6F4. Avenir Next and JetBrains Mono; original partner logos.'))
    print('Restyled lesson',L['n'])

from build_teacher_books import generate
generate()
