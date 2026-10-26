"""Check the delivered teacher volumes, navigation, content and printed pages."""
from pathlib import Path
import json,re
import pdfplumber
from pypdf import PdfReader
from content import LESSONS
import build_course as B
from build_teacher_books import NAMES,DEST,OUT,COURSE_TITLE

def normal(s):
    return re.sub(r'\s+','',s).replace('\u00ad','').replace('`','').replace('’',"'").replace('‘',"'").replace('−','-')

report=[]
qa={'volumes':[]}
for name in NAMES:
    source=(DEST/f'{name}.tex').read_text()
    reader=PdfReader(OUT/f'{name}.pdf')
    assert reader.metadata.title.startswith(COURSE_TITLE),(name,'course title metadata')
    # Every lesson has a resolved PDF destination and a live contents link.
    dests=reader.named_destinations
    labels=re.findall(r'\\newlabel\{lesson-(\d)\}\{\{[^}]*\}\{(\d+)\}',(OUT/f'{name}.aux').read_text())
    assert len(labels)==5,(name,labels)
    starts={int(n):int(p) for n,p in labels}
    assert list(starts)==list(range(1,6)) and list(starts.values())==sorted(starts.values())
    texts=[]
    with pdfplumber.open(OUT/f'{name}.pdf') as pdf:
        for index,page in enumerate(pdf.pages,1):
            txt=page.extract_text() or '';texts.append(txt)
            assert '??' not in txt,(name,index,'unresolved reference')
            for c in page.chars:
                if c['text'].strip():assert c['x0']>=-1 and c['x1']<=page.width+1 and c['top']>=-1 and c['bottom']<=page.height+1,(name,index,'text outside page')
            if index>1:
                footer=''.join(c['text'] for c in page.chars if c['top']>page.height-40 and c['x0']>page.width-85)
                assert str(index) in footer,(name,index,footer,'page numbering')
        assert pdf.pages[0].images,(name,'cover illustration')
        assert normal('Dynamic Programming') in normal(texts[0])
        assert normal('From Recursion to Efficient Solutions') in normal(texts[0])
    for L in LESSONS:
        n=L['n'];start=starts[n];stop=starts.get(n+1,len(texts)+1)-1
        body='\n'.join(texts[start-1:stop]);flat=normal(body)
        for u in L['units']:
            assert u['id'] in body,(name,u['id'])
            if name=='teacher-class-notes':
                for key in ('q','a','hint','mis'):
                    assert normal(u[key]) in flat,(name,u['id'],key,'text missing')
        if name=='teacher-class-notes':
            for u in L['units']:
                for fn in B.codes(u):assert B.precode(fn).rstrip() in source,(name,n,fn,'code missing')
            assert f'Lesson\\%20{n}/lesson.ipynb' in source
        else:
            assert 'colab.research.google.com' not in source
        assert f'{start}' in texts[1]
    for page in reader.pages:
        for ref in page.get('/Annots',[]):
            annot=ref.get_object();action=annot.get('/A',{})
            target=action.get('/D') if action.get('/S')=='/GoTo' else annot.get('/Dest')
            if isinstance(target,str):assert target in dests,(name,target,'broken link')
    qa['volumes'].append(dict(name=name,pages=len(texts),lesson_pages=starts))
    report.append(f'{name}: {len(texts)} pages; five lessons, all {sum(len(L["units"]) for L in LESSONS)} IDs, continuous page numbers and internal links checked.')
(OUT/'verified-layout.json').write_text(json.dumps(qa,indent=2))
Path('teacher-books-verification.txt').write_text('\n'.join(report)+'\n')
print('\n'.join(report))
