"""Build reproducible text datasets, student skeletons and separate solutions."""
from pathlib import Path
from collections import deque
import inspect, json, math, random, shutil
import programs as P
ROOT = Path(__file__).resolve().parent.parent
MOD = 1_000_000_007
SPECS = {
 1:[('staircase','stairs_table','n','Return the exact number of ordered routes to step n using jumps 1 or 2.'),
    ('stride13','stairs_13','n','Return the exact number of ordered routes to step n using jumps 1 or 3.'),
    ('frog','frog_table','heights','Return the minimum total height-difference cost to the last stone.'),
    ('frog-path','frog_path','heights','Return (cost, path), with stone indices from start to finish. On equal candidate costs keep predecessor i - 1.')],
 2:[('dice','dice_table','n','Count ordered sequences of faces 1..6 with total n, modulo MOD.'),
    ('dice123','dice_123','n','Count ordered sequences of faces 1..3 with total n, modulo MOD.'),
    ('grid','grid_table','rows','Count top-left to bottom-right paths moving right or down, modulo MOD. A star is blocked.')],
 3:[('tower','tower_table','bosses','Return the fewest points your friend pays. Your friend goes first; each turn takes 1 or 2 bosses.'),
    ('array','array_rolling','values, m','Count fillings of missing zeros using 1..m, neighbours differing by at most 1; modulo MOD.')],
 4:[('feast','feast_table','limit, a, b','Return the greatest reachable fullness, eating a or b and drinking water at most once.')],
 5:[('hps','hps_table','john, budget','Return the greatest number of wins using at most budget changes. First gesture is free.')],
}

# One description per problem, shared by PRACTICE.txt and the tutor book's
# practice chapter so the two cannot drift apart.
INFO = {
 'frog-path':dict(name='Frog: recover a route',format='Line 1: n. Line 2: the n heights.',answer='Pair (cost, path); path lists stone indices. Ties keep predecessor i - 1.',
     edges=['A single stone: cost 0 and path [0].','Equal heights: keep i - 1 at each tie, returning every stone index.','Two cheapest routes: keep the predecessor i - 1 when final costs tie.']),
 'staircase':dict(name='Staircase',format='One line: the target step n.',answer='Exact integer (no modulo).',
     edges=['n = 0: the empty route counts once, so the answer is 1.','n = 1: only one jump of 1; the program must not read step -1.']),
 'stride13':dict(name='Staircase with jumps 1 or 3',format='One line: the target step n.',answer='Exact integer (no modulo).',
     edges=['n = 0: the empty route counts once, so the answer is 1.','n = 2: only 1 + 1 fits, because a jump of 3 overshoots; the answer is 1.']),
 'frog':dict(name='Frog',format='Line 1: n, the number of stones. Line 2: the n heights.',answer='Minimum total cost.',
     edges=['Two stones of equal height: one jump costing 0, and there is no stone i - 2 to read.']),
 'dice':dict(name='Dice Combinations',format='One line: the target total n.',answer='Count modulo 1,000,000,007.',
     edges=['n = 1: a single throw of 1; the answer is 1.','n = 7: the first total above the largest face, so all six faces fit; the answer is 1 + 2 + 4 + 8 + 16 + 32 = 63.']),
 'dice123':dict(name='Dice with faces 1 to 3',format='One line: the target total n.',answer='Count modulo 1,000,000,007.',
     edges=['n = 1: only the face 1 fits; the answer is 1.']),
 'grid':dict(name='Grid Paths',format='Line 1: n. Then n lines of n characters: . is open and * is blocked.',answer='Count modulo 1,000,000,007.',
     edges=['A 1 by 1 grid whose only cell is blocked: the start is blocked, so the answer is 0.','A 1 by 1 open grid: the start is the finish, so the answer is 1.']),
 'tower':dict(name='Mortal Kombat Tower',format='Line 1: t, the number of towers. For each tower: a line with n, then a line with n boss types (0 easy, 1 hard).',answer='One line per tower: the fewest points your friend pays.',
     edges=['One hard boss: your friend must take it and pays 1; taking two bosses is out of range.','One easy boss: your friend pays 0; taking two bosses is out of range.']),
 'array':dict(name='Array Description',format='Line 1: n and m. Line 2: the n entries, with 0 for a missing value.',answer='Count modulo 1,000,000,007.',
     edges=['Fixed values 1 and 3 next to each other (m = 3): they differ by 2, so no filling exists and the answer is 0.','A single missing entry with m = 3: any of 1, 2, 3 fits, so the answer is 3.']),
 'feast':dict(name='Fruit Feast',format='One line: limit a b.',answer='Greatest reachable fullness.',
     edges=['limit 8, fruits 4 and 6: 4 + 4 reaches the limit without water; the answer is 8.','limit 5, both fruits 4: water cannot help, so the answer is 4.','limit 10, fruits 4 and 7 (the lesson example): without water the best is 8; 7, drink to 3, then 7 reaches 10.']),
 'hps':dict(name='Hoof, Paper, Scissors',format='Line 1: n and the switch budget K. Then n lines, each H, P or S (John\'s gestures).',answer='Most rounds won.',
     edges=['HHH with budget 0: keep one gesture; P wins all three rounds, so the answer is 3.','A single round S with an unused budget of 2: the answer is 1.']),
}
CROSSCHECK = {
 1:'Expected outputs were cross-checked by forward propagation, an independent\nformulation of the same rules.',
 2:'Expected outputs were cross-checked by forward propagation; the open\n1,000 by 1,000 grid uses a binomial coefficient.',
 3:'Expected outputs were cross-checked by forward propagation over (position, turn)\nfor Tower and by a dictionary of ending values for Array Description.',
 4:'Expected outputs were cross-checked by a breadth-first search over\n(fullness, water used) states and, separately, by enumerating how many fruits\nof each size are eaten before and after the drink. In small, medium and large\nthe answer is below the limit, so a program that just returns the limit fails.',
 5:'Expected outputs were cross-checked by forward propagation over\n(switches used, previous gesture); large HPS has 21 constant runs, so 20\nswitches win every round.',
}
RECURSION_TEXT=('Python stops recursion at about 1,000 nested calls by default. A recursive\n'
 'solution (cached or not) is for the small and edge files only; on medium and\n'
 'large files it may stop with RECURSION LIMIT or run out of time. Use an\n'
 'iterative loop for those.')

def size_detail(problem,args):
    if problem in ('staircase','stride13','dice','dice123'):return f'target {args[0]:,}'
    if problem=='feast':return f'limit {args[0]:,}; fruits {args[1]:,} and {args[2]:,}'
    if problem=='array':return f'{len(args[0]):,} entries; m = {args[1]}'
    if problem=='grid':return f'{len(args[0]):,} by {len(args[0]):,} grid'
    if problem=='hps':return f'{len(args[0]):,} rounds; budget {args[1]}'
    if problem=='frog':return f'{len(args[0]):,} stones'
    if problem=='tower':return f'{len(args[0]):,} bosses'
    return f'{len(args[0]):,} entries'

def feast_counts(t,a,b):
    # Alternative formulation: choose how many fruits of each size come before the
    # drink, then how many after it. No table scans or state search.
    dry={x*a+y*b for x in range(t//a+1) for y in range((t-x*a)//b+1)}
    best=max(dry)
    for d in dry:
        best=max([best]+[d//2+v for v in dry if d//2+v<=t])
    return best

def oracle(problem, args):
    # Independent formulations: propagate forward, enumerate choices, or use a closed form.
    if problem in ('staircase','stride13','dice','dice123'):
        n=args[0]; jumps={'staircase':(1,2),'stride13':(1,3),'dice':range(1,7),'dice123':range(1,4)}[problem]
        a=[0]*(n+1);a[0]=1
        for i in range(n+1):
            for step in jumps:
                if i+step<=n:
                    a[i+step]+=a[i]
                    if problem.startswith('dice'): a[i+step]%=MOD
        return a[n]
    if problem in ('frog','frog-path'):
        h=args[0];a=[math.inf]*len(h);a[0]=0;previous=[-1]*len(h)
        for i in range(len(h)):
            for j in (i+1,i+2):
                if j<len(h):
                    candidate=a[i]+abs(h[j]-h[i])
                    # Forward propagation reaches i - 1 last, so replace ties here.
                    if candidate<=a[j]:a[j]=candidate;previous[j]=i
        if problem=='frog-path':
            path=[];i=len(h)-1
            while i!=-1:path.append(i);i=previous[i]
            return a[-1],path[::-1]
        return a[-1]
    if problem=='grid':
        rows=args[0];n=len(rows)
        if all(set(row)=={'.'} for row in rows): return math.comb(2*n-2,n-1)%MOD
        a=[[0]*n for _ in rows]
        if rows[0][0]=='.':a[0][0]=1
        for r in range(n):
            for c in range(n):
                for rr,cc in ((r+1,c),(r,c+1)):
                    if rr<n and cc<n and rows[rr][cc]=='.':a[rr][cc]=(a[rr][cc]+a[r][c])%MOD
        return a[-1][-1]
    if problem=='tower':
        a=args[0];n=len(a);d=[[math.inf]*2 for _ in range(n+1)];d[0][0]=0
        for i in range(n):
            for turn in (0,1):
                for take in (1,2):
                    if i+take<=n:d[i+take][1-turn]=min(d[i+take][1-turn],d[i][turn]+(sum(a[i:i+take]) if turn==0 else 0))
        return min(d[n])
    if problem=='array':
        values,m=args;before={v:1 for v in range(1,m+1) if values[0] in (0,v)}
        for given in values[1:]:
            now={}
            for v,count in before.items():
                for nxt in (v-1,v,v+1):
                    if 1<=nxt<=m and given in (0,nxt):now[nxt]=(now.get(nxt,0)+count)%MOD
            before=now
        return sum(before.values())%MOD
    if problem=='feast':
        t,a,b=args
        seen={(0,False)};q=deque(seen)
        while q:
            f,w=q.popleft();nxt=[(f+a,w),(f+b,w)]+([] if w else [(f//2,True)])
            for state in nxt:
                if state[0]<=t and state not in seen:seen.add(state);q.append(state)
        return max(f for f,w in seen)
    if problem=='hps':
        john,k=args
        if len(john)==100000:
            # Twenty-one constant runs. Twenty switches match every winning gesture.
            assert sum(a!=b for a,b in zip(john,john[1:]))==20 and k==20
            return len(john)
        # Forward propagation of each (used, previous) state rather than pulling candidates.
        d={(0,''):0};beat={'H':'S','P':'H','S':'P'}
        for opp in john:
            nxt={}
            for (used,old),score in d.items():
                for g in 'HPS':
                    u=used+int(bool(old) and old!=g)
                    if u<=k:nxt[u,g]=max(nxt.get((u,g),-1),score+int(beat[g]==opp))
            d=nxt
        return max(d.values())

def encode(p,args):
    if p in ('staircase','stride13','dice','dice123'):return f'{args[0]}\n'
    if p in ('frog','frog-path'):return f'{len(args[0])}\n'+ ' '.join(map(str,args[0]))+'\n'
    if p=='grid':return f'{len(args[0])}\n'+'\n'.join(args[0])+'\n'
    if p=='tower':return f'1\n{len(args[0])}\n'+' '.join(map(str,args[0]))+'\n'
    if p=='array':return f'{len(args[0])} {args[1]}\n'+' '.join(map(str,args[0]))+'\n'
    if p=='feast':return ' '.join(map(str,args))+'\n'
    if p=='hps':return f'{len(args[0])} {args[1]}\n'+'\n'.join(args[0])+'\n'

def datasets(p,rng):
    if p=='frog-path':return datasets('frog',random.Random(211126))
    if p in ('staircase','stride13'):return [(5,),(100,),(10000,)]
    if p in ('dice','dice123'):return [(3 if p=='dice' else 5,),(1000,),(1000000,)]
    if p=='frog':return [([20,50,30,40,10,10],),([rng.randint(1,10000) for _ in range(500)],),([rng.randint(1,10000) for _ in range(100000)],)]
    if p=='grid':
        rows=[''.join('.' if r==0 or c==29 or rng.random()>.15 else '*' for c in range(30)) for r in range(30)]
        return [(['...','.*.','...'],),(rows,),(['.'*1000]*1000,)]
    if p=='tower':return [([1,0,1,1],),([rng.randrange(2) for _ in range(1000)],),([rng.randrange(2) for _ in range(200000)],)]
    if p=='array':return [([2,0,0,1],3),([0 if i%11 else 3 for i in range(1000)],10),([0]*100000,100)]
    # Every feast size has its answer below the limit, and water is needed.
    if p=='feast':return [(15,8,9),(10000,2527,2945),(5000000,743782,939000)]
    if p=='hps':return [('HHSSP',1),(''.join(rng.choice('HPS') for _ in range(1000)),5),(''.join('HPS'[i%3]*(4762 if i<20 else 4760) for i in range(21)),20)]

EDGES={'staircase':[(0,),(1,)],'stride13':[(0,),(2,)],'frog':[([8,8],)],'dice':[(1,),(7,)],'dice123':[(1,)],'grid':[(['*'],),(['.'],)],'tower':[([1],),([0],)],'array':[([1,3],3),([0],3)],'feast':[(8,4,6),(5,4,4),(10,4,7)],'hps':[('HHH',0),('S',2)]}

EDGES['frog-path']=[([7],),([7,7,7],),([10,30,20,40],)]

def build(only=None):
    rng=random.Random(261024)
    for lesson,specs in SPECS.items():
        if only is not None and lesson not in only:continue
        folder=ROOT/f'Lesson {lesson}';tests=folder/'test-cases';tests.mkdir(exist_ok=True)
        from build_course import constants_for
        header='"""Lesson '+str(lesson)+': file-based practice. Run with --help for test options."""\n'+constants_for([fn for _,fn,*_ in specs],imports=False)+'\n'
        starter=header;solution=header;manifest=[]
        for problem,fn,signature,description in specs:
            name=fn
            starter+=f'def {name}({signature}):\n    """{description}"""\n    # Write your solution here. Return the answer; do not print it.\n    raise NotImplementedError\n\n\n'
            code=inspect.getsource(getattr(P,fn)).replace('def '+fn+'(', 'def '+name+'(')
            solution+=code+'\n\n'
            sub=tests/problem;sub.mkdir(exist_ok=True)
            instances=list(zip(['small','medium','large'],datasets(problem,rng)))
            instances += [(f'edge-{i+1}',args) for i,args in enumerate(EDGES[problem])]
            assert len(INFO[problem]['edges'])==len(EDGES[problem]),problem
            for label,args in instances:
                expected=oracle(problem,args)
                actual=getattr(P,fn)(*args)
                assert actual==expected,(lesson,problem,label,actual,expected)
                if problem=='feast':
                    assert feast_counts(*args)==expected,(label,args)
                    if label in ('small','medium','large'): assert expected<args[0],(label,'answer must be below the limit')
                (sub/f'{label}.in').write_text(encode(problem,args))
                (sub/f'{label}.out').write_text(str(expected)+'\n')
                manifest.append(dict(problem=problem,size='small' if label.startswith('edge') else label,input=f'{problem}/{label}.in',output=f'{problem}/{label}.out'))
        mapping='{'+', '.join(repr(p)+': '+fn for p,fn,*_ in specs)+'}'
        footer='if __name__ == "__main__":\n    import sys\n    sys.dont_write_bytecode = True  # keep the folder free of __pycache__\n    from runner import main\n    raise SystemExit(main('+mapping+'))\n'
        (folder/'starter.py').write_text(starter+footer);(folder/'solution.py').write_text(solution+footer)
        shutil.copy2(Path(__file__).with_name('runner_template.py'),folder/'runner.py')
        (tests/'manifest.json').write_text(json.dumps(manifest,indent=2))
        names=[p for p,*_ in specs]
        readme=f'''LESSON {lesson}: FILE-BASED PRACTICE

Edit starter.py. Each named function receives parsed data and returns its answer.
The loader and test runner are ready; no solution is imported by the starter.
Keep runner.py and test-cases/ beside starter.py.

python3 starter.py                         # all small and edge tests
python3 starter.py --problem PROBLEM --size medium
python3 starter.py --problem PROBLEM --size large
python3 starter.py --size all              # all sizes and edge tests
python3 starter.py --problem PROBLEM --file test-cases/PROBLEM/small.in
python3 solution.py --size all             # teacher's completed solution

Replace PROBLEM with {"one of: "+", ".join(names) if len(names)>1 else names[0]}.
Paths in the default suite are resolved relative to runner.py, so running from
another working directory works. A --file path is relative to your current directory.
Each .in has a matching .out containing the expected answer, not an algorithm.
The runner compares answers and prints PASS or FAIL, never silently treating an
unfinished function as a pass. Each case runs in a separate process. Default timeout:
30 seconds per case; change it with --timeout 60 if your machine needs longer.
A timeout or RecursionError is reported so a slow attempt does not stop later cases.
Timing includes process startup and is not an online-judge performance guarantee.

RECURSION
{RECURSION_TEXT}

FORMAT
'''
        for problem in names:
            info=INFO[problem]
            readme+=f"{problem}: {info['name']}\n  Input:  {info['format']}\n  Answer: {info['answer']}\n"
        if lesson in (4,5):
            readme+='The local runner reads the named .in file; the separate programs/ adapters\nkeep the original judge filenames ('+('feast.in / feast.out' if lesson==4 else 'hps.in / hps.out')+').\n'
        readme+='\nEDGE FILES (run with the small tests)\n'
        for problem in names:
            for i,text in enumerate(INFO[problem]['edges'],1):
                readme+=f'{problem}/edge-{i}.in: {text}\n'
        readme+='\nDATASET SIZES\n'
        for problem in names:
            for size,args in zip(['small','medium','large'],datasets(problem,random.Random(261024))):
                readme+=f'{problem:12} {size:6} {size_detail(problem,args)}\n'
        readme+='\n'+CROSSCHECK[lesson]+'\n'
        (folder/'PRACTICE.txt').write_text(readme)
        print(f'Lesson {lesson}: {len(specs)} starter functions, {len(manifest)} checked files.',flush=True)
if __name__=='__main__':build()
