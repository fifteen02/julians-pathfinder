"""Check the current illustrated slides and render them for review."""
from pathlib import Path
from collections import Counter
import hashlib
import io
import json
import re
import subprocess
import zipfile

import pdf_compat as pdfplumber
from PIL import Image, ImageDraw
from slide_illustrations import ILLUSTRATIONS

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / 'Course source'
OUT = HERE / 'illustration-qa'
OUT.mkdir(exist_ok=True)
report = []

for n in range(1, 6):
    current = HERE / f'build/Lesson {n}/slides.pdf'
    renders = []
    with pdfplumber.open(current) as after:
        links = [h.get('uri') for h in after.pages[0].hyperlinks]
        assert f'https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%20{n}/lesson.ipynb' in links
        seen = set()
        for i, new in enumerate(after.pages, 1):
            newtext = new.extract_text() or ''
            for c in new.chars:
                assert c['x0'] >= -1 and c['x1'] <= new.width + 1 and c['top'] >= -1 and c['bottom'] <= new.height + 1, (n, i, 'text outside page')
            header = next((line for line in newtext.splitlines() if re.search(r'L\d-\d\d / (QUESTION|ANSWER)', line)), '')
            match = re.search(r'(L\d-\d\d) / (QUESTION|ANSWER)', header)
            key = (match[1], match[2] == 'ANSWER') if match else None
            if key in ILLUSTRATIONS and 'PYTHON' not in header:
                seen.add(key)
                assert len(new.images) == 1, (n, i, 'illustration missing')
                for img in new.images:
                    # The image bounding rectangle must not collide with any text.
                    for c in new.chars:
                        hit = c['x0'] < img['x1'] - 1 and c['x1'] > img['x0'] + 1 and c['top'] < img['bottom'] - 1 and c['bottom'] > img['top'] + 1
                        assert not hit, (n, i, 'image/text collision', c['text'])
                prefix = OUT / f'L{n}-slide-{i:02}'
                subprocess.run(['pdftoppm', '-f', str(i), '-l', str(i), '-singlefile', '-scale-to', '1600', '-png', str(current), str(prefix)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                renders.append((prefix.with_suffix('.png'), f'{key[0]} / {match[2]} / slide {i}'))
        assert seen == {key for key in ILLUSTRATIONS if key[0].startswith(f'L{n}-')}
        report.append(f'Lesson {n}: {len(after.pages)} slides; {len(seen)} illustrations; page bounds and Colab link checked.')
    sheet = Image.new('RGB', (1600, 480 * ((len(renders) + 1) // 2)), '#ddd9d0')
    draw = ImageDraw.Draw(sheet)
    for j, (path, label) in enumerate(renders):
        im = Image.open(path).convert('RGB')
        im.thumbnail((780, 440))
        x, y = j % 2 * 800 + 10, j // 2 * 480 + 30
        sheet.paste(im, (x, y))
        draw.text((x, y - 22), label, fill='black')
    sheet.save(OUT / f'Lesson-{n}-illustrations.png')

(HERE / 'illustrations-verification.txt').write_text('\n'.join(report) + '\n')
print('\n'.join(report))
