from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, json
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parent.parent
from compile_all import build_dir
OUT=ROOT/'Course source/qa';OUT.mkdir(exist_ok=True)
def job(args):
    n,kind=args; directory=build_dir(n)/f'render-{kind}';directory.mkdir(exist_ok=True)
    for stale in directory.glob('p-*.png'): stale.unlink()
    subprocess.run(['pdftoppm','-scale-to','1100','-png',str(build_dir(n)/f'{kind}.pdf'),str(directory/'p')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    paths=sorted(directory.glob('p-*.png'))
    per=12 if kind=='slides' else 8
    cols=3 if kind=='slides' else 4
    w=600 if kind=='slides' else 400
    h=360 if kind=='slides' else 590
    for stale in OUT.glob(f'L{n}-{kind}-*.png'): stale.unlink()
    for start in range(0,len(paths),per):
        group=paths[start:start+per];rows=(len(group)+cols-1)//cols
        sheet=Image.new('RGB',(cols*w,rows*h),'#ddd9d0');draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(group):
            im=Image.open(path).convert('RGB');im.thumbnail((w-12,h-28))
            x=(j%cols)*w+(w-im.width)//2;y=(j//cols)*h+22
            sheet.paste(im,(x,y));draw.text(((j%cols)*w+8,(j//cols)*h+4),f'L{n} {kind} p{start+j+1}',fill='black')
        sheet.save(OUT/f'L{n}-{kind}-{start//per+1}.png')
    return (n,kind,len(paths))
with ThreadPoolExecutor(max_workers=4) as pool:
    r=list(pool.map(job,[(n,k) for n in range(1,6) for k in ['tutorial','teacher','worksheet-printer-friendly','slides']]))
print(r)
(OUT/'counts.json').write_text(json.dumps(r))
