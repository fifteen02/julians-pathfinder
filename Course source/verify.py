from pathlib import Path
from itertools import product
from collections import deque
from functools import lru_cache
import random, json, contextlib, io, subprocess, tempfile, math
import programs as P
from content import LESSONS
ROOT=Path(__file__).resolve().parent.parent
checks=0

def check(actual, expected, label):
    global checks
    assert actual==expected,(label,actual,expected)
    checks+=1

def frog_brute(h):
    def walk(i,cost):
        if i==len(h)-1: return cost
        return min(walk(j,cost+abs(h[j]-h[i])) for j in (i+1,i+2) if j<len(h))
    return walk(0,0)
def tower_brute(a):
    def walk(i,friend,paid):
        if i==len(a): return paid
        return min(walk(i+k,not friend,paid+(sum(a[i:i+k]) if friend else 0)) for k in (1,2) if i+k<=len(a))
    return walk(0,True,0)
def array_brute(a,m):
    return sum(all(a[i] in (0,v[i]) for i in range(len(a))) and all(abs(v[i]-v[i-1])<=1 for i in range(1,len(a))) for v in product(range(1,m+1),repeat=len(a)))
def feast_bfs(t,a,b):
    seen={(0,False)}; queue=deque(seen)
    while queue:
        f,w=queue.popleft()
        neighbours=[(f+a,w),(f+b,w)]
        if not w: neighbours.append((f//2,True))
        for state in neighbours:
            if state[0]<=t and state not in seen: seen.add(state);queue.append(state)
    return max(f for f,w in seen)
def hps_brute(john,k):
    return max(sum(P.BEATS[g]==j for g,j in zip(seq,john)) for seq in product('HPS',repeat=len(john)) if sum(seq[i]!=seq[i-1] for i in range(1,len(seq)))<=k) if john else 0

for n in range(21):
    check(P.sum_to(n), n * (n + 1) // 2, ('sum_to', n))
    check(P.sum_squares(n), n * (n + 1) * (2 * n + 1) // 6, ('sum_squares', n))
    check(P.power2(n), 2 ** n, ('power2', n))
    check(P.factorial(n), math.factorial(n), ('factorial', n))
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        P.countdown(n)
    check(printed.getvalue().splitlines(), [str(k) for k in range(n, 0, -1)] + ['Go!'], ('countdown', n))

for n in range(16):
    check(P.stairs_cached(n),P.stairs_slow(n),('stairs cache',n))
    check(P.stairs_table(n),P.stairs_slow(n),('stairs table',n))
check([P.stairs_13(n) for n in range(8)],[1,1,1,2,3,4,6,9],'stride 1 3')
for n in range(1,7):
    for h in product([10,20,30],repeat=n):
        want=frog_brute(h)
        for fn in [P.frog_slow,P.frog_cached,P.frog_table]: check(fn(h),want,(fn.__name__,h))
for n in range(11):
    want=P.dice_slow(n)
    for fn in [P.dice_cached,P.dice_table,P.dice_window]:check(fn(n),want,(fn.__name__,n))
for n in range(1,3):
    for cells in product('.*',repeat=n*n):
        rows=[''.join(cells[r*n:(r+1)*n]) for r in range(n)]
        for fn in [P.grid_cached,P.grid_table]: check(fn(rows),P.grid_slow(rows),(fn.__name__,rows))
for bits in product('.*',repeat=9):
    rows=[''.join(bits[i:i+3]) for i in range(0,9,3)]
    check(P.grid_table(rows),P.grid_slow(rows),('grid',rows))
for n in range(1,8):
    for a in product([0,1],repeat=n):
        for fn in [P.tower_cached,P.tower_table]:check(fn(a),tower_brute(a),(fn.__name__,a))
rng=random.Random(261024)
for _ in range(200):
    n=rng.randrange(1,6);m=rng.randrange(1,5);a=[rng.randrange(m+1) for i in range(n)]
    want=array_brute(a,m)
    for fn in [P.array_cached,P.array_full,P.array_rolling]:check(fn(a,m),want,(fn.__name__,a,m))
for t in range(1,20):
    for a in range(1,t+1):
        for b in range(a,t+1):
            want=feast_bfs(t,a,b)
            for fn in [P.feast_cached,P.feast_table]:check(fn(t,a,b),want,(fn.__name__,t,a,b))
for n in range(1,6):
    for john in product('HPS',repeat=n):
        for k in range(min(2,n)+1):
            want=hps_brute(john,k)
            for fn in [P.hps_cached,P.hps_table]:check(fn(john,k),want,(fn.__name__,john,k))
for L in LESSONS:
    dest=ROOT/f'Lesson {L["n"]}'
    for filename in ['lesson.ipynb','teacher-notebook.ipynb']:
        nb=json.loads((dest/filename).read_text());ns={}
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in nb['cells']:
                if cell['cell_type']=='code': exec(compile(cell['source'],filename,'exec'),ns)
        checks+=1
    for ex in L['exercises']:
        for args,want in ex['tests']: check(getattr(P,ex['solution'])(*eval(args)),want,(ex['id'],args))
# Useful larger tests for iterative implementations only.
check(P.frog_table([7]*100000),0,'large frog')
check(P.dice_table(1000),937196411,'dice1000')
check(P.dice_window(100000),797925478,'dice100000')
check(P.array_rolling([0]*10000,1),1,'large array')
check(P.tower_table([1]*10000),(10000+2)//3,'large tower')
check(P.hps_table('H'*10000,20),10000,'large hps')
# Judge wrappers use original classroom sample data stored locally.
briefs=json.loads((ROOT/'Course source/problem_briefs.json').read_text())
names=['frog_table','dice_table','grid_table','tower_table','array_rolling','feast_table','hps_table']
for i,name in enumerate(names):
    n=[1,2,2,3,3,4,5][i]
    with tempfile.TemporaryDirectory() as work:
        inp=briefs[i][7];want=briefs[i][8]
        if name in ['feast_table','hps_table']:
            stem='feast' if name=='feast_table' else 'hps'
            Path(work,f'{stem}.in').write_text(inp)
            r=subprocess.run(['python3',str(ROOT/f'Lesson {n}/programs/{name}.py')],cwd=work,capture_output=True,text=True,check=True)
            actual=Path(work,f'{stem}.out').read_text().strip()
        else:
            r=subprocess.run(['python3',str(ROOT/f'Lesson {n}/programs/{name}.py')],cwd=work,input=inp,capture_output=True,text=True,check=True)
            actual=r.stdout.strip()
        check(actual,want,('judge wrapper',name))
import verify_task_intent
import verify_recursion_reveal
import verify_frog_path
import verify_dice_memory

print(f'PASS: {checks} checks, including independent small-case searches, 10 complete notebook executions and all 7 judge adapters.')
(ROOT/'Course source/verification.txt').write_text(f'PASS: {checks} checks. All 10 notebooks execute; all 7 judge adapters match the classroom samples.\n')
