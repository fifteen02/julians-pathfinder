"""Check current Colab links, covers, question coverage and page bounds."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import hashlib,io,json,re,subprocess,contextlib
import pdf_compat as pdfplumber
from PIL import Image,ImageDraw
from content import LESSONS
from candies_style import colab_url
from compile_all import build_dir
ROOT=Path(__file__).resolve().parent.parent
HERE=Path(__file__).resolve().parent
QA=HERE/'colab-qa';QA.mkdir(exist_ok=True)
KINDS=('worksheet-printer-friendly','teacher','slides')

def check(job):
 n,kind=job; path=build_dir(n)/(kind+'.pdf')
 with pdfplumber.open(path) as pdf:
  pages=[p.extract_text(x_tolerance=1) or '' for p in pdf.pages]
  assert colab_url(n) in [a.get('uri') for a in pdf.pages[0].hyperlinks],(n,kind,'link')
  assert pdf.pages[0].images,(n,kind,'cover art')
  for u in LESSONS[n-1]['units']:assert u['id'] in '\n'.join(pages),(n,kind,u['id'])
  if kind=='worksheet-printer-friendly':
   text='\n'.join(pages);assert not re.search(r'\b(?:Name|Date)\s*:',text)
  for i,p in enumerate(pdf.pages):
   for c in p.chars:
    if c['text'].strip():assert c['x0']>=-1 and c['x1']<=p.width+1 and c['top']>=-1 and c['bottom']<=p.height+1,(n,kind,i,c)
  count=len(pages)
 directory=build_dir(n)/f'render-colab-{kind}';directory.mkdir(exist_ok=True)
 last=3 if kind=='worksheet-printer-friendly' else 1
 subprocess.run(['pdftoppm','-f','1','-l',str(last),'-scale-to','1200','-png',str(path),str(directory/'p')],check=True)
 return dict(lesson=n,kind=kind,pages=count,colab=colab_url(n),layout='passed')

if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4) as pool:report=list(pool.map(check,[(n,k) for n in range(1,6) for k in KINDS]))
 for n in range(1,6):
  selected=[]
  for k in KINDS:
   directory=build_dir(n)/f'render-colab-{k}'
   selected += [(f'Lesson {n} / {k} / {p.stem}',p) for p in sorted(directory.glob('p-*.png'))]
  width,height=500,730;cols=3
  sheet=Image.new('RGB',(cols*width,height*((len(selected)+cols-1)//cols)),'#ddd9d0');draw=ImageDraw.Draw(sheet)
  for j,(label,p) in enumerate(selected):
   im=Image.open(p).convert('RGB');im.thumbnail((width-14,height-32))
   x=(j%cols)*width+(width-im.width)//2;y=(j//cols)*height+25
   sheet.paste(im,(x,y));draw.text(((j%cols)*width+7,(j//cols)*height+5),label,fill='black')
  sheet.save(QA/f'Lesson-{n}.png')
 (HERE/'colab-verification.txt').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: all 15 cover links point to the matching student notebook; covers illustrated; all question IDs present and text inside page bounds.')
