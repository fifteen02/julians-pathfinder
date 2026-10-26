from pathlib import Path
import subprocess, concurrent.futures, json, shutil, os
ROOT=Path(__file__).resolve().parent.parent
HERE=Path(__file__).resolve().parent
KINDS=['tutorial','teacher','worksheet-printer-friendly','worksheet_answers','slides']

def build_dir(n):
    """Compiler output, logs and QA renders live here, never inside a lesson folder."""
    folder=HERE/'build'/f'Lesson {n}'
    folder.mkdir(parents=True,exist_ok=True)
    return folder

def source_path(n, kind):
    """Teacher lesson sources are build intermediates, not classroom handouts."""
    return (build_dir(n) if kind in ('tutorial', 'teacher') else ROOT/f'Lesson {n}')/f'{kind}.tex'


def clean_stray(lessons=range(1,6)):
    """Remove __pycache__ from the lessons and Course source, and any old Lesson N/build."""
    removed=[]
    roots=[ROOT/f'Lesson {n}' for n in lessons]+[HERE]
    for root in roots:
        for path in sorted(root.rglob('__pycache__'),reverse=True):
            if any(part in ('.qa-venv','.qa-jupyter') for part in path.relative_to(root).parts): continue
            shutil.rmtree(path,ignore_errors=True);removed.append(path)
    for n in lessons:
        old=ROOT/f'Lesson {n}'/'build'
        if old.exists(): shutil.rmtree(old);removed.append(old)
    return removed

def pdf_pages(path):
    """Return [(text, chars, width, height)] with chars as dicts holding text/x0/x1/top/bottom.
    Uses pdfplumber when installed, otherwise PyMuPDF."""
    try:
        import pdfplumber
    except ImportError:
        import fitz
        out=[]
        with fitz.open(path) as doc:
            for page in doc:
                chars=[]
                for block in page.get_text('rawdict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            for c in span['chars']:
                                x0,top,x1,bottom=c['bbox']
                                chars.append(dict(text=c['c'],x0=x0,x1=x1,top=top,bottom=bottom))
                out.append((page.get_text(),chars,page.rect.width,page.rect.height))
        return out
    with pdfplumber.open(path) as pdf:
        return [(p.extract_text() or '',p.chars,p.width,p.height) for p in pdf.pages]

def compile_one(job):
    n,kind=job; dest=ROOT/f'Lesson {n}'; out=build_dir(n); log=out/f'{kind}-compile.txt'
    for attempt in range(2):
        r=subprocess.run(['/Library/TeX/texbin/xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(out),str(source_path(n,kind))],cwd=dest,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log.write_text(r.stdout)
        if r.returncode:
            return dict(lesson=n,kind=kind,ok=False,tail=r.stdout[-1700:])
    warnings=[line for line in (out/f'{kind}.log').read_text().splitlines() if any(x in line for x in ['Overfull','Missing character','undefined'])]
    return dict(lesson=n,kind=kind,ok=True,warnings=warnings)
if __name__=='__main__':
    jobs=[(n,k) for n in range(1,6) for k in KINDS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(compile_one,jobs))
    (HERE/'compile-report.json').write_text(json.dumps(results,indent=2))
    for r in results: print(json.dumps(r))

    from build_teacher_books import build as build_teacher_books
    build_teacher_books()
