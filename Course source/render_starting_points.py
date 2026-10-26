"""Render the changed question slides and recursion introduction for visual QA."""
from pathlib import Path
import subprocess
import pdf_compat as pdfplumber
from PIL import Image, ImageDraw
from sheet_guidance import IMPLEMENT
from compile_all import build_dir
OUT = Path(__file__).resolve().parent / 'starting-points-qa'
OUT.mkdir(exist_ok=True)
items = []
for n in range(1,6):
    source = build_dir(n) / 'slides.pdf'
    with pdfplumber.open(source) as doc:
        for i,p in enumerate(doc.pages,1):
            text = p.extract_text() or ''
            selected = any(ident + ' / QUESTION' in text for ident in IMPLEMENT)
            if selected or n == 1 and 3 <= i <= 12:
                name = OUT / f'L{n}-slide-{i:02}'
                subprocess.run(['pdftoppm','-f',str(i),'-l',str(i),'-singlefile','-scale-to','1600','-png',str(source),str(name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                items.append((name.with_suffix('.png'),f'Lesson {n}, slide {i}'))
for a in range(0,len(items),6):
    group = items[a:a+6]
    canvas = Image.new('RGB',(1800,540*((len(group)+1)//2)),'#ddd9d0')
    draw = ImageDraw.Draw(canvas)
    for j,(path,label) in enumerate(group):
        im = Image.open(path).convert('RGB');im.thumbnail((880,495))
        x,y=(j%2)*900+10,(j//2)*540+30
        canvas.paste(im,(x,y));draw.text((x,y-22),label,fill='black')
    canvas.save(OUT/f'review-{a//6+1}.png')
print(f'Rendered {len(items)} changed slides for review.')
