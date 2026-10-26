"""Verify question IDs and full prompts across published classroom formats.

Run after compilation and before publish.py. Tutor books use narrative rather
than repeating every prompt, so their classroom references are checked by ID.
"""
from pathlib import Path
import json
import re
import unicodedata
from content import LESSONS
from compile_all import build_dir, pdf_pages

ROOT = Path(__file__).resolve().parent.parent

def normal(text):
    text = unicodedata.normalize('NFKD', text).casefold()
    return ''.join(c for c in text if c.isalnum())

report = []
for lesson in LESSONS:
    n = lesson['n']
    units = lesson['units']
    ids = [u['id'] for u in units]
    folder = ROOT / f'Lesson {n}'
    for name in ('lesson', 'teacher-notebook'):
        nb = json.loads((folder / f'{name}.ipynb').read_text())
        sections = {}
        current = None
        for cell in nb['cells']:
            text = ''.join(cell['source'])
            match = re.match(r'## (L\d-\d\d): ', text)
            if match:
                current = match[1]
                sections[current] = []
            if current:
                sections[current].append(text)
        assert list(sections) == ids, (n, name, 'IDs/order')
        for u in units:
            assert sections[u['id']][0].endswith(u['q']), (n, name, u['id'], 'prompt')
        if n == 1:
            assert 'Write frog_table(heights) using a loop.' in sections['L1-18'][0]
            assert 'Test your frog_table(heights) from L1-18.' in sections['L1-19'][0]
            if name == 'lesson':
                assert any(t.startswith('def frog_table(heights):') for t in sections['L1-18']), 'Frog implementation must be in L1-18'
                assert not any(t.startswith('def frog_table(heights):') for t in sections['L1-19']), 'L1-19 must reuse the student implementation'
                assert '**Use your `frog_table` from L1-18.**' in '\n'.join(sections['L1-19'])
        for ident, texts in sections.items():
            for target, function in re.findall(r'in (L\d-\d\d) as `([^`]+)`', '\n'.join(texts)):
                assert target in sections, (n, name, ident, 'missing target', target)
                assert any(re.search(r'^def ' + re.escape(function) + r'\(', t, re.M) for t in sections[target]), (n, name, ident, target, function)
    kinds = ('teacher', 'worksheet-printer-friendly', 'worksheet_answers', 'slides')
    pages = {kind: [p[0] for p in pdf_pages(build_dir(n) / f'{kind}.pdf')] for kind in kinds}
    for kind, texts in pages.items():
        for u in units:
            candidates = [i + 1 for i, text in enumerate(texts) if normal(u['q']) in normal(text) and u['id'] in text]
            assert candidates, (n, kind, u['id'], 'ID/full prompt not together on a page')
            if n == 1 and u['id'] in ('L1-15', 'L1-19'):
                report.append(f"{u['id']} | {u['title']} | {kind} page {candidates[0]}")
    book = '\n'.join(p[0] for p in pdf_pages(build_dir(n) / 'tutorial.pdf'))
    assert all(ident in book for ident in ids), (n, 'tutor book references')
    report.append(f'Lesson {n}: {len(ids)} IDs and full prompts match both notebooks and all four classroom PDFs; tutor-book references and deferred-code links valid.')
Path('alignment-verification.txt').write_text('\n'.join(report) + '\n')
print('\n'.join(report))
