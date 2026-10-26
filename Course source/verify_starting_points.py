"""Check implementation starting points against the actual delivered code and PDFs."""
from pathlib import Path
import ast
import inspect
import json
import re
from content import LESSONS
from sheet_guidance import IMPLEMENT
from compile_all import build_dir, pdf_pages
import programs as P
import starting_points as SP

ROOT = Path(__file__).resolve().parent.parent

def signatures(source):
    tree = ast.parse(source)
    return {node.name: [(child.name, ast.dump(child.args)) for child in ast.walk(node)
                        if isinstance(child, ast.FunctionDef)]
            for node in tree.body if isinstance(node, ast.FunctionDef)}

def compact(text):
    return re.sub(r'\s+', '', text).replace('\u00ad', '')

checked = 0
for L in LESSONS:
    folder = ROOT / f'Lesson {L["n"]}'
    full = signatures((folder / 'solutions.py').read_text())
    practice = signatures((folder / 'solution.py').read_text())
    starter = signatures((folder / 'starter.py').read_text())
    for fn in practice:
        if fn in full:
            assert practice[fn] == full[fn], (fn, 'practice signature mismatch')
            assert starter[fn] == full[fn], (fn, 'starter signature mismatch')
    nb = json.loads((folder / 'lesson.ipynb').read_text())
    notebook_source = '\n'.join(c['source'] for c in nb['cells'] if c['cell_type'] == 'code')
    notebook_defs = signatures(notebook_source)
    texts = {kind: [p[0] for p in pdf_pages(build_dir(L['n']) / f'{kind}.pdf')]
             for kind in ('worksheet-printer-friendly', 'teacher', 'slides')}
    for u in L['units']:
        ident = u['id']
        if ident not in IMPLEMENT:
            continue
        fns, hints = IMPLEMENT[ident]
        assert 1 <= len(hints) <= 3, ident
        for fn in fns:
            expected = signatures(inspect.getsource(getattr(P, fn)))[fn]
            assert full[fn] == expected, (ident, fn, 'reference')
            assert notebook_defs[fn] == expected, (ident, fn, 'notebook')
            assert len(SP.RETURNS[fn]) == len(expected), (ident, fn, 'return descriptions')
            setup, final = SP.outer_wiring(fn)
            if final:
                node = next(node for node in ast.parse(notebook_source).body if isinstance(node, ast.FunctionDef) and node.name == fn)
                assert ast.dump(node.body[-1]) == ast.dump(ast.parse(final).body[0]), (ident, fn, 'outer return wiring')
            notebook_text = '\n'.join(c['source'] for c in nb['cells'])
            for call, meaning in SP.RETURNS[fn]:
                assert meaning in notebook_text, (ident, fn, 'missing return meaning')
        # Signatures must be with this question, not only in an appendix.
        for kind, pages in texts.items():
            if kind == 'slides':
                question = next(p for p in pages if ident + ' / QUESTION' in p)
            else:
                alltext = '\n'.join(pages)
                # Match the exercise block; teacher timetable may mention a range.
                marker = re.search(r'(?m)^' + ident + r'(?:\s*/|\s+[A-Z])', alltext)
                assert marker, (ident, kind, 'question block')
                question = alltext[marker.start():]
                next_id = re.search(r'(?m)^L\d-\d\d(?:\s*/|\s+[A-Z])', question[len(ident):])
                if next_id:
                    question = question[:len(ident) + next_id.start()]
            for fn in fns:
                lines = [line.strip() for line in inspect.getsource(getattr(P, fn)).splitlines()
                         if line.strip().startswith('def ')]
                for line in lines:
                    assert compact(line) in compact(question), (ident, kind, line)
            assert 'returns' in question.lower(), (ident, kind, 'return descriptions')
            assert 'Hints' in question, (ident, kind, 'hints')
        checked += 1
    for name in ('worksheet.tex', 'worksheet.pdf'):
        assert not (folder / name).exists(), (folder, 'retired worksheet still active')

message = f'PASS: {checked} implementation questions; exact outer/nested signatures checked in reference code, notebook stubs and all three printed formats; return meanings and outer helper calls supplied; 1-3 hints each. No regular worksheets remain in the active lessons.'
Path('starting-points-verification.txt').write_text(message + '\n')
print(message)
