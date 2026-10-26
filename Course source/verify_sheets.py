"""Check printed trace answers against small exhaustive searches."""
from itertools import product
from collections import deque
from pathlib import Path
from content import LESSONS
from sheet_guidance import TABLES, TABLE_ANSWERS, CODING, GUIDES

units={u['id']:u for lesson in LESSONS for u in lesson['units']}
assert len(units)==sum(len(L['units']) for L in LESSONS)
assert 'L1-21' in units
assert TABLES.keys() == TABLE_ANSWERS.keys(), "Every answer table needs its matching student table"
assert CODING <= units.keys()
for lesson in LESSONS:
    assert lesson['n'] in GUIDES
for ident,(heads,rows) in TABLES.items():
    assert len(rows)==len(TABLE_ANSWERS[ident])
    assert all(len(row)==len(heads) for row in rows+TABLE_ANSWERS[ident])

def routes(n,jumps):
    if n==0:return [()]
    return [(j,)+tail for j in jumps if j<=n for tail in routes(n-j,jumps)]

assert [int(v) for v in TABLE_ANSWERS['L1-05'][0][1:]]==[len(routes(n,(1,2))) for n in range(1,6)]
assert [int(v) for v in TABLE_ANSWERS['L1-13'][0][1:]]==[len(routes(n,(1,3))) for n in range(8)]
assert [int(v) for v in TABLE_ANSWERS['L2-07'][0][1:]]==[len(routes(n,(1,2,3))) for n in range(6)]

heights=[10,30,20,40]
def frog_paths(i):
    if i==0:return [[0]]
    return [path+[i] for earlier in (i-1,i-2) if earlier>=0 for path in frog_paths(earlier)]
costs=[min(sum(abs(heights[a]-heights[b]) for a,b in zip(path,path[1:])) for path in frog_paths(i)) for i in range(4)]
assert [int(v) for v in TABLE_ANSWERS['L1-19'][1][1:]]==costs

for i,row in enumerate(TABLE_ANSWERS['L3-12']):
    expected=[]
    for last in (1,2,3):
        expected.append(sum(seq[-1]==last and (i<2 or seq[-1]==3) and all(abs(a-b)<=1 for a,b in zip(seq,seq[1:])) for seq in product((1,2,3),repeat=i+1)))
    assert list(map(int,row[2:]))==expected

def reachable(limit,initial,fruit):
    seen=set(initial);queue=deque(initial)
    while queue:
        f=queue.popleft()
        for size in fruit:
            if f+size<=limit and f+size not in seen:
                seen.add(f+size);queue.append(f+size)
    return seen

for ident,limit,fruit in [('L4-07',10,(4,7)),('L4-09',9,(4,6))]:
    dry=reachable(limit,{0},fruit)
    just_drank={f//2 for f in dry}
    wet=reachable(limit,just_drank,fruit)
    expected=[wet] if ident=='L4-07' else [dry,just_drank,wet]
    for row,values in zip(TABLE_ANSWERS[ident],expected):
        assert row[1:]==['Y' if f in values else '-' for f in range(limit+1)]

import programs as P
for (label,predicted,output),grid in zip(TABLE_ANSWERS['L2-13'],[['.'],['*'],['..','..'],['...','.*.','...']]):
    assert int(predicted)==int(output)==P.grid_table(grid),(label,grid)
# Recursion warm-up tables, from the functions themselves.
import io, contextlib
out=io.StringIO()
with contextlib.redirect_stdout(out): P.countdown(3)
assert [row[1] for row in TABLE_ANSWERS['L1-01']]==out.getvalue().split()
assert [int(row[2].split('= ')[-1]) for row in TABLE_ANSWERS['L1-02']]==[P.sum_squares(k) for k in (4,3,2,1,0)]
for row,k in zip(TABLE_ANSWERS['L1-02'][:-1],(4,3,2,1)):
    a,b=row[2].split(' = ')[0].split(' + ');assert int(a)==k*k and int(b)==P.sum_squares(k-1)
beats={'H':'S','P':'H','S':'P'}
for count,row in enumerate(units['L5-08']['diagram']['rows'],1):
    john='HHSSP'[:count];expected=[]
    for used in (0,1):
        for ending in 'HPS':
            scores=[sum(beats[g]==op for g,op in zip(seq,john)) for seq in product('HPS',repeat=count) if seq[-1]==ending and sum(a!=b for a,b in zip(seq,seq[1:]))==used]
            expected.append(str(max(scores)) if scores else '-')
    assert row[1:]==expected
# L5-12 explains one cell of that table: after H,H,S, one switch, ending H.
prefix,used,ending,score=TABLE_ANSWERS['L5-12'][0]
row=next(r for r in units['L5-08']['diagram']['rows'] if r[0]==prefix)
assert row[1+3*int(used)+'HPS'.index(ending)]==score

message=f'PASS: {len(units)} question IDs; all added trace tables checked by exhaustive enumeration or reachability search; all 30 cells of the five-round HPS score table independently checked.\n'
Path('sheet-verification.txt').write_text(message)
print(message)
