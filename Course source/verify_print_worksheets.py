"""Check and render the compact student worksheets without regenerating other material."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import io,json,re,subprocess
import pdf_compat as pdfplumber
from PIL import Image,ImageDraw
from content import LESSONS
from build_course import tex
from compile_all import build_dir
ROOT=Path(__file__).resolve().parent.parent
QA=Path(__file__).resolve().parent/'print-qa';QA.mkdir(exist_ok=True)
def check(L):
 n=L['n'];source=(ROOT/f'Lesson {n}/worksheet-printer-friendly.tex').read_text()
 for u in L['units']:assert tex(u['q']) in source,(n,u['id'],'question changed')
 for bad in ('Name:', 'Date:', 'Working / explanation:', 'STUDENT WORKSHEET','\\begin{lstlisting}', '\\leaders'):
  assert bad not in source,(n,bad)
 path=build_dir(n)/'worksheet-printer-friendly.pdf'
 with pdfplumber.open(path) as pdf:
  texts=[p.extract_text(x_tolerance=1) or '' for p in pdf.pages]
  text='\n'.join(texts)
  actual=re.findall(r'^(L\d-\d\d)\s*/',text,re.M)
  assert actual==[u['id'] for u in L['units']],(n,actual)
  assert pdf.pages[0].images,(n,'missing illustrated cover')
  for index,page in enumerate(pdf.pages):
   if index: assert not page.images,(n,'decorative bitmap in question pages')
   for c in page.chars:
    if c['text'].strip():assert 0<=c['x0']<c['x1']<=page.width and 0<=c['top']<c['bottom']<=page.height,(n,c)
  count=len(pdf.pages)
  assert count > 1  # cover and question pages; signatures may add pages
 directory=build_dir(n)/'render-print';directory.mkdir(exist_ok=True)
 for stale in directory.glob('p-*.png'):stale.unlink()
 subprocess.run(['pdftoppm','-scale-to','1500','-png',str(path),str(directory/'p')],check=True)
 paths=sorted(directory.glob('p-*.png'))
 sheet=Image.new('RGB',(600*len(paths),875),'#ddd9d0');draw=ImageDraw.Draw(sheet)
 for j,p in enumerate(paths):
  im=Image.open(p).convert('RGB');im.thumbnail((588,840))
  sheet.paste(im,(j*600+(600-im.width)//2,25));draw.text((j*600+8,5),f'Lesson {n}: page {j+1}',fill='black')
 sheet.save(QA/f'Lesson-{n}.png')
 return dict(lesson=n,pages=count,questions=len(L['units']),wording='unchanged',bounds='passed')
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(check,LESSONS))
 Path('print-worksheet-verification.txt').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
