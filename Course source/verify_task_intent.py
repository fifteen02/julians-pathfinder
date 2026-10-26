"""Catch writing-vs-testing mismatches in prompts and actual notebook sections."""
import ast
import json
import re
from pathlib import Path
from content import LESSONS
from sheet_guidance import IMPLEMENT, REUSE, CODING
from build_course import DEFERRED_CODE

ROOT = Path(__file__).resolve().parent.parent
assert CODING == set(IMPLEMENT)
assert not (IMPLEMENT.keys() & REUSE.keys())
report = []
for lesson in LESSONS:
    units = {u['id']: u for u in lesson['units']}
    sections = {}
    current = None
    nb = json.loads((ROOT / f"Lesson {lesson['n']}" / 'lesson.ipynb').read_text())
    for cell in nb['cells']:
        source = ''.join(cell['source'])
        heading = re.match(r'## (L\d-\d\d): ', source)
        if heading:
            current = heading[1]
            sections[current] = []
        if current:
            sections[current].append((cell['cell_type'], source))
    introduced = {}
    for ident, unit in units.items():
        cells = sections[ident]
        text = '\n'.join(s for _, s in cells)
        defs = {node.name: node for kind, s in cells if kind == 'code'
                for node in ast.parse(s).body if isinstance(node, ast.FunctionDef)}
        stubs = {name for name, node in defs.items()
                 if any(isinstance(x, ast.Return) and isinstance(x.value, ast.Constant)
                        and x.value.value is None for x in ast.walk(node))}
        requested = set(IMPLEMENT.get(ident, ([], []))[0])
        assert stubs == requested, (ident, 'stub/task mismatch', stubs, requested)
        if requested:
            assert re.search(r'\b(write|implement|add that base case)\b', unit['q'], re.I), (ident, 'missing explicit coding request')
            assert '**No code here.**' not in text, ident
            for fn in requested:
                assert fn + '(' in unit['q'], (ident, fn, 'unnamed function in prompt')
                assert fn not in introduced, (ident, fn, 'overwrites an earlier implementation')
                assert any(kind == 'code' and 'checks = [' in s and fn + '(' in s for kind, s in cells), (ident, fn, 'missing checks')
                introduced[fn] = ident
            mode = 'WRITE ' + ', '.join(sorted(requested))
        elif ident in REUSE:
            fn, earlier = REUSE[ident]
            assert introduced.get(fn) == earlier, (ident, 'implementation not introduced')
            assert earlier in unit['q'] and fn + '(' in unit['q'], (ident, 'implicit reuse')
            assert re.search(r'\btest\b', unit['q'], re.I), (ident, 'missing test instruction')
            assert '**Start with:**' not in text and fn not in defs, (ident, 'duplicate scaffold')
            assert f'**Use your `{fn}` from {earlier}.**' in text, ident
            assert any(kind == 'code' and 'checks = [' in s and fn + '(' in s for kind, s in cells), (ident, 'missing test cell')
            mode = f'TEST {fn} from {earlier}'
        else:
            mode = 'REASON / TRACE' + ('; labelled worked example' if defs else '')
            if defs:
                if unit.get('given'):
                    assert set(defs) == {unit['given']} and '**Code to trace:**' in text, (ident, 'unlabelled trace code')
                else:
                    assert '**Worked example:' in text, (ident, 'unlabelled solution')
        report.append(f'{ident}: {mode}')
    # Cached Frog is a worked example; the following task asks for iteration.
    if lesson['n'] == 1:
        text = '\n'.join(s for _, s in sections['L1-17'])
        assert 'def frog_cached(heights):' in text and '**No code here.**' not in text
    for (n, fn), target in DEFERRED_CODE.items():
        if n == lesson['n']:
            assert target in IMPLEMENT and target in sections, (fn, target)
Path('task-intent-verification.txt').write_text('\n'.join(report) + '\n')
print(f'PASS: {len(report)} questions reviewed; {len(IMPLEMENT)} explicit implementation tasks and {len(REUSE)} reuse/test tasks match their notebook sections.')
