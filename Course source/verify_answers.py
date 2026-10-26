from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, re, io, contextlib, json
from compile_all import build_dir, pdf_pages
from PIL import Image, ImageDraw
from content import LESSONS
from sheet_guidance import TABLES
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'Course source/answers-qa'
OUT.mkdir(exist_ok=True)

def verify(L):
 n=L['n'];dest=ROOT/f'Lesson {n}'
 tex=(dest/'worksheet_answers.tex').read_text()
 # A diagram or table referenced by a question must precede its answer.
 visuals=0
 for u in L['units']:
  marker=r'\qtopic{'+u['id']+(' / OPTIONAL EXTENSION' if u['extension'] else '')+'}'
  section=tex.split(marker,1)[1].split(r'\qtopic{',1)[0]
  question,answer=section.split(r'\textbf{Worked answer.}',1)
  d=u.get('diagram')
  needs=u['id'] in TABLES or (d and d['kind'] in ('table','tree','lastmove'))
  if needs:
   assert 'supplied with the question.' in question,(n,u['id'])
   assert r'\begin{tikzpicture}' in question or r'\begin{tabularx}' in question,(n,u['id'])
   visuals+=1
 # Every implementation and its example must run without other lesson code.
 # Each program is printed once, numbered: One complete Python implementation, the
 # numbered listing, its check and the expected output.
 pairs=re.findall(r'One complete Python implementation: [^\n]*?\\par\n\\begin\{lstlisting\}\[style=numbered\]\n(.*?)\\end\{lstlisting\}.*?\\textbf\{Check\.\}.*?\\begin\{lstlisting\}\n(.*?)\\end\{lstlisting\}.*?\\textbf\{Expected output\.\}.*?\\begin\{lstlisting\}\[language=\{\}\]\n(.*?)\\end\{lstlisting\}',tex,re.S)
 implementations=tex.count('One complete Python implementation:')
 assert len(pairs)==implementations,(n,len(pairs),implementations)
 programs={}
 for code,run,want in pairs:
  namespace={}; out=io.StringIO()
  with contextlib.redirect_stdout(out):
   exec(code,namespace);exec(run,namespace)
  assert out.getvalue().strip()==want.strip(),(n,run,out.getvalue(),want)
  programs.update({k:code for k,v in namespace.items() if callable(v) and k in code})
 # A later question that reuses a program names it and has its own check, run
 # against the listing printed earlier in this booklet.
 reuses=re.findall(r'Same implementation as (L\d-\d\d)\} \(\\texttt\{([^}]*)\}.*?\\textbf\{Check\.\}.*?\\begin\{lstlisting\}\n(.*?)\\end\{lstlisting\}.*?\\textbf\{Expected output\.\}.*?\\begin\{lstlisting\}\[language=\{\}\]\n(.*?)\\end\{lstlisting\}',tex,re.S)
 assert len(reuses)==tex.count('Same implementation as'),(n,'reuse')
 for earlier,fn,run,want in reuses:
  fn=fn.replace(r'\_','_')
  assert fn in programs and tex.index(r'\label{ans-'+fn+'}')<tex.index('Same implementation as '+earlier),(n,fn)
  namespace={}; out=io.StringIO()
  with contextlib.redirect_stdout(out):
   exec(programs[fn],namespace);exec(run,namespace)
  assert out.getvalue().strip()==want.strip(),(n,run,out.getvalue(),want)
 if True:
  pdf=pdf_pages(build_dir(n)/'worksheet_answers.pdf')
  texts=[p[0] for p in pdf]
  alltext='\n'.join(texts)
  ids=re.findall(r'^(L[1-5]-[0-9]{2})(?:/OPTIONALEXTENSION)?$',alltext.replace(' ',''),re.M)
  assert ids==[u['id'] for u in L['units']],(n,'question order',ids)
  assert len(re.findall(r'Worked\s*answer\.',alltext))==len(L['units'])
  outside=[]
  for i,(text,chars,width,height) in enumerate(pdf):
   for c in chars:
    if c['text'].strip() and (c['x0']<0 or c['x1']>width or c['top']<0 or c['bottom']>height): outside.append((i+1,c['text']))
  assert not outside,(n,outside[:10])
  count=len(pdf)
 directory=build_dir(n)/'render-worksheet_answers';directory.mkdir(exist_ok=True)
 for p in directory.glob('p-*.png'):p.unlink()
 subprocess.run(['pdftoppm','-scale-to','1100','-png',str(build_dir(n)/'worksheet_answers.pdf'),str(directory/'p')],check=True)
 paths=sorted(directory.glob('p-*.png'))
 for start in range(0,len(paths),8):
  group=paths[start:start+8];sheet=Image.new('RGB',(1600,590*((len(group)+3)//4)),'#ddd9d0');draw=ImageDraw.Draw(sheet)
  for j,path in enumerate(group):
   im=Image.open(path).convert('RGB');im.thumbnail((388,562))
   x=(j%4)*400+(400-im.width)//2;y=(j//4)*590+22
   sheet.paste(im,(x,y));draw.text(((j%4)*400+8,(j//4)*590+4),f'Lesson {n} answers page {start+j+1}',fill='black')
  sheet.save(OUT/f'L{n}-{start//8+1}.png')
 return {'lesson':n,'pages':count,'answers':len(L['units']),'standalone_code_checks':len(pairs),'reused_program_checks':len(reuses),'question_visuals_before_answers':visuals,'question_order':'passed','page_bounds':'passed'}
if __name__ == '__main__':
 with ThreadPoolExecutor(max_workers=4) as pool:
  result=list(pool.map(verify,LESSONS))
 Path('answers-verification.txt').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
