from pathlib import Path
import json,re
from compile_all import build_dir, pdf_pages
from content import LESSONS
ROOT=Path(__file__).resolve().parent.parent
report=[]
for L in LESSONS:
    n=L['n']; ids=[u['id'] for u in L['units']]
    for kind in ['tutorial','teacher','worksheet-printer-friendly','worksheet_answers','slides']:
        path=build_dir(n)/f'{kind}.pdf'
        if True:
            pdf=pdf_pages(path)
            pages=[p[0] for p in pdf]
            for ident in ids:
                assert ident in '\n'.join(pages),(path,ident)
            outside=[]
            for i,(text,chars,width,height) in enumerate(pdf):
                for c in chars:
                    if c['text'].strip() and (c['x0'] < -1 or c['x1']>width+1 or c['top'] < -1 or c['bottom'] >height+1):
                        outside.append((i+1,c['text']))
            assert not outside,(path,outside[:10])
            if kind=='slides':
                questions=[(i,re.search(r'(L\d-\d{2}) / QUESTION',t).group(1)) for i,t in enumerate(pages) if re.search(r'L\d-\d{2} / QUESTION',t)]
                assert [x[1] for x in questions]==ids
                for i,ident in questions: assert ident+' / ANSWER' in pages[i+1],(path,ident)
            report.append(f'Lesson {n} {kind}: {len(pages)} pages; every question ID present; all text inside page'+('; each question immediately followed by its answer' if kind=='slides' else ''))
Path('pdf-verification.txt').write_text('\n'.join(report)+'\n')
print('\n'.join(report))
