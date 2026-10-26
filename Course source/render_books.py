from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent
from compile_all import build_dir
OUT=ROOT/'Course source/book-qa';OUT.mkdir(exist_ok=True)
def render(n):
    folder=build_dir(n)/'book-render';folder.mkdir(exist_ok=True)
    for p in folder.glob('p-*.png'):p.unlink()
    subprocess.run(['pdftoppm','-scale-to','1300','-png',str(build_dir(n)/'tutorial.pdf'),str(folder/'p')],check=True)
    paths=sorted(folder.glob('p-*.png'))
    for p in OUT.glob(f'L{n}-*.png'):p.unlink()
    for start in range(0,len(paths),6):
        group=paths[start:start+6];sheet=Image.new('RGB',(1500,720*((len(group)+2)//3)),'#ddd9d0');d=ImageDraw.Draw(sheet)
        for j,p in enumerate(group):
            im=Image.open(p).convert('RGB');im.thumbnail((488,688));x=(j%3)*500+(500-im.width)//2;y=(j//3)*720+25
            sheet.paste(im,(x,y));d.text(((j%3)*500+8,(j//3)*720+5),f'Lesson {n} / page {start+j+1}',fill='black')
        sheet.save(OUT/f'L{n}-{start//6+1}.png')
    return (n,len(paths))
if __name__ == '__main__':
    import sys
    lessons = [int(x) for x in sys.argv[1:]] or list(range(1, 6))
    with ThreadPoolExecutor(max_workers=3) as pool:
        counts = list(pool.map(render, lessons))
    saved = dict(json.loads((OUT/'counts.json').read_text())) if (OUT/'counts.json').exists() else {}
    saved.update(dict(counts))
    (OUT/'counts.json').write_text(json.dumps(sorted(saved.items())))
    print(counts)
