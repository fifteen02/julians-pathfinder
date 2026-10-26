"""Slow down the bridges from a concrete example to a state and its code.

These are tutor-only additions. Classroom questions and their IDs stay unchanged.
Every numerical example is calculated here, with small independent enumerations
checked against the reference implementations where the full problem is solved.
"""
from functools import lru_cache
from itertools import product
import programs as P
from book_blocks import table, figure


def cache_walkthrough():
    cache = {0: 1}
    rows = []
    def ways(step):
        if step < 0:
            rows.append([f'ways({step})', 'negative target', 'return 0; store nothing'])
            return 0
        if step in cache:
            rows.append([f'ways({step})', f'key {step} already exists', f'return {cache[step]}; make no smaller calls'])
            return cache[step]
        rows.append([f'ways({step})', f'key {step} is missing', f'wait for ways({step-1}) and ways({step-2})'])
        a, b = ways(step-1), ways(step-2)
        cache[step] = a+b
        rows.append([f'ways({step}) resumes', f'{a} + {b} = {a+b}', f'store cache[{step}] = {a+b}; return {a+b}'])
        return a+b
    answer = ways(3)
    assert answer == P.stairs_cached(3)
    assert P.stairs_cached(4)==5
    return [
        'Before reading the cached program, follow a request for step 3. The dictionary initially contains only `cache[0] = 1`. In the table, a missing key causes more calls; a present key supplies an answer immediately. A row saying that a call resumes means its smaller calls have returned.',
        table(['Call being handled', 'What is known', 'What this call does'], rows),
        f'The first request for step 1 computes its answer and stores it. When ways(3) later asks for step 1 again, that second request reads the stored {cache[1]}. It does not call ways(0) or ways(-1) again. The call still happens; the repeated work inside it is what disappears.',
        'Read `cache[1] = 1` as two different pieces of information: key 1 identifies the target step, and the stored 1 counts routes. They happen to be equal here. At step 3 they differ: `cache[3] = 3` is another coincidence, whereas `cache[4] = 5` would mean five routes to step 4. The dictionary never stores the next step to visit.'
    ]


def frog_walkthrough():
    heights = [20, 50, 30, 40, 10, 10]
    costs = [P.frog_table(heights[:i+1]) for i in range(len(heights))]
    def routes(destination):
        if destination==0:return [[0]]
        return [route+[destination] for jump in (1,2) if destination>=jump
                for route in routes(destination-jump)]
    earlier=[]
    for destination in (2,3):
        for route in routes(destination):
            jumps=[abs(heights[b]-heights[a]) for a,b in zip(route,route[1:])]
            earlier.append([str(destination),' to '.join(map(str,route)),
                            ' + '.join(map(str,jumps))+f' = {sum(jumps)}'])
        assert costs[destination]==min(sum(abs(heights[b]-heights[a]) for a,b in zip(r,r[1:])) for r in routes(destination))
    rows=[]
    for j in (3, 2):
        jump=abs(heights[4]-heights[j]);total=costs[j]+jump
        rows.append([f'from stone {j}', f'cost({j}) = {costs[j]}',
                     f'abs({heights[4]} - {heights[j]}) = {jump}', f'{costs[j]} + {jump} = {total}'])
    diagram=r'''\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,every node/.style={font=\small,align=center}]
\node[draw=quiet,fill=codepaper,text width=5cm,minimum height=12mm] (a) at (0,0) {Reach stone 3, then jump to 4\\20 already paid + 30 = 50};
\node[draw=quiet,fill=codepaper,text width=5cm,minimum height=12mm] (b) at (0,-1.8) {Reach stone 2, then jump to 4\\10 already paid + 20 = 30};
\node[draw=ink,text width=4cm,minimum height=14mm] (c) at (6.1,-.9) {Cheapest cost to stone 4\\min(50, 30) = 30};
\draw[->] (a.east)--(c.west);\draw[->] (b.east)--(c.west);
\end{tikzpicture}'''
    assert costs[4] == min(costs[j]+abs(heights[4]-heights[j]) for j in (3,2)) == 30
    return [
        'Work one destination before writing the general rule. Use heights [20, 50, 30, 40, 10, 10] and destination stone 4, whose height is 10. There are exactly two possible last jumps: from stone 3 or stone 2. We first need the cheapest total cost to each starting stone. List every route to those two stones; each summand below is the absolute difference between the heights at the ends of one jump.',
        table(['Destination stone','Route from stone 0','Jump costs and total'],earlier),
        'The smallest total for stone 2 is 10, and the smallest for stone 3 is 20. Now extend each cheapest route by its final jump into stone 4. The starting stone changes, so both the cost already paid and the cost of the new jump must be checked.',
        table(['Last jump', 'Cost before this jump', 'Cost of this jump', 'Whole-route candidate'], rows),
        figure(diagram, 'Both arrows offer a complete cost for reaching the same destination. The smaller total becomes the returned answer; the program does not add the two alternatives.'),
        'The returned 30 is an amount of effort. It is not stone 30, height 30, or the instruction to jump 30 places. Stone 4 is the input to this question; 30 is its answer. The expression below repeats this same two-candidate calculation for any destination i. If i is 1, only the previous stone exists. If i is 0, the frog is already at its destination and has paid nothing.'
    ]


def dice_walkthrough():
    ways=[P.dice_table(t) for t in range(4)]
    running=0;rows=[]
    for face in range(1,7):
        if face<=3:
            prior=running;running+=ways[3-face]
            rows.append([str(face),f'ways[{3-face}] = {ways[3-face]}',f'{prior} + {ways[3-face]} = {running}'])
        else:
            rows.append([str(face),'does not fit; do not read a list entry',f'unchanged: {running}'])
    assert running==P.dice_table(3)==4
    return [
        'Trace the inner loop on target total 3. The completed earlier entries are `ways[0] = 1`, `ways[1] = 1` and `ways[2] = 2`. The new entry `ways[3]` starts at 0. Each legal final face contributes one earlier count; the table shows the running value of this one entry.',
        table(['Final face tried', 'Earlier count read', 'New value of ways[3]'],rows),
        'The face-3 contribution is the single sequence [3]: append 3 to the empty sequence counted by `ways[0]`. It has already been included. Adding another 1 after the sum would count [3] twice. Faces 4, 5 and 6 contribute nothing to target 3 because the final throw alone would overshoot; they are not extra ways of reaching 3.',
        'After the inner loop, `ways[3]` is a completed answer. Only then does the outer loop move to target 4. For that next target, the already completed `ways[3]` will be one of the earlier counts. We reuse its value; we do not reset earlier entries.'
    ]


def tower_walkthrough():
    bosses=[1,0,1,1]
    @lru_cache(None)
    def cost(i,friend):
        if i==len(bosses):return 0
        return min((sum(bosses[i:i+t]) if friend else 0)+cost(i+t,not friend)
                   for t in (1,2) if i+t<=len(bosses))
    rows=[]
    for friend in (True,False):
        for take in (1,2):
            pay=sum(bosses[2:2+take]) if friend else 0
            later=cost(2+take,not friend)
            rows.append(['friend' if friend else 'you',str(take),str(pay),
                         f'cost({2+take}, {not friend}) = {later}',f'{pay} + {later} = {pay+later}'])
    assert cost(0,True)==P.tower_cached(bosses)==P.tower_table(bosses)
    return [
        'Use bosses [1, 0, 1, 1], where 1 means hard and 0 means easy. Focus on position i = 2: bosses at positions 0 and 1 are finished; bosses at positions 2 and 3 remain. The value returned by cost(2, friend_turn) counts only skip points still needed. Points already spent on earlier bosses are not included again.',
        'Compare two situations at that same position. In the first, the friend acts next and pays for hard bosses taken now. In the second, you act next and pay nothing for the bosses taken now. After either player takes one or two bosses, the other player takes the next turn. True names the friend\'s turn; False names yours.',
        table(['Turn now','Take','Pay now','Cheapest later cost','Candidate total'],rows),
        f'On the friend\'s turn, compare 1 and 2: return {cost(2,True)}. On your turn, compare 1 and 0: return {cost(2,False)}. The same position therefore has two different answers. A cache keyed only by position 2 would have no way to keep both. The turn is part of the question, not part of the numerical cost.',
        'The end position is i = 4, just after the last boss. There are no bosses left for either player, so both end-state answers are 0. This is why a candidate that takes the last two bosses adds 0 as its later cost. It does not mean those bosses were free for the friend.'
    ]


def array_walkthrough():
    values=[2,0,0,1];m=3
    def prefixes(length):
        return [list(a) for a in product(range(1,m+1),repeat=length)
                if all(values[i] in (0,a[i]) for i in range(length))
                and all(abs(a[i]-a[i-1])<=1 for i in range(1,length))]
    before=prefixes(2);after=prefixes(3)
    rows=[]
    for v in range(1,4):
        group=[a for a in before if a[-1]==v]
        rows.append([str(v),', '.join(map(str,group)),str(len(group)),', '.join(str(a+[2]) for a in group)])
    count=sum(a[-1]==2 for a in after)
    final=prefixes(4)
    assert count==3 and len(final)==P.array_rolling(values,m)==5
    diagram=r'''\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,every node/.style={font=\small,align=center}]
\node[draw=quiet,text width=4cm] (a) at (0,0) {[2, 1] becomes [2, 1, 2]};
\node[draw=quiet,text width=4cm] (b) at (0,-1.1) {[2, 2] becomes [2, 2, 2]};
\node[draw=quiet,text width=4cm] (c) at (0,-2.2) {[2, 3] becomes [2, 3, 2]};
\node[draw=ink,fill=codepaper,text width=4.5cm,minimum height=17mm] (d) at (6,-1.1) {Position 2, ending value 2\\stored count = 1 + 1 + 1 = 3};
\draw[->] (a.east)--(d.west);\draw[->] (b.east)--(d.west);\draw[->] (c.east)--(d.west);
\end{tikzpicture}'''
    return [
        'Use input `values = [2, 0, 0, 1]` and `m = 3`. An input 0 marks an unfilled position; the permitted values are 1, 2 and 3. A prefix here is the filled beginning of the array, not a prefix sum. We are counting beginnings, not adding their entries.',
        'Calculate the cell at position i = 2 for ending value 2. This position is the third place because positions start at 0. At the previous position, the possible filled beginnings are [2, 1], [2, 2] and [2, 3]. Each may be followed by 2: the neighbouring difference is at most 1.',
        table(['Earlier ending value','Earlier beginnings','Count read','Append the chosen value 2'],rows),
        figure(diagram,'Three different beginnings reach the same cell. The cell stores their count, while its position and ending value identify which beginnings belong there.'),
        'Thus `table[2][2] = 3`. The first 2 selects a position; the second 2 selects a value allowed at that position; 3 counts the beginnings in this group. Storing only the value 2 would lose how many different arrays led here.',
        'This differs from the recursive question count(i, previous). That function asks how many ways the unfinished end can be completed, assuming the preceding value is already fixed. The table instead asks how many ways the beginning could have been filled to reach this cell. Both count arrays, but from opposite ends. We must derive the table update from its own meaning, rather than copy a recursive argument into a table index without explaining it.',
        f'The fixed last entry 1 accepts earlier endings 1 or 2. The completed final row contains {len(final)} valid arrays in all; P.array_rolling returns that count. The value 0 used to mark an unknown input never becomes an entry in any completed array.' .replace('P.array_rolling','array_rolling')
    ]


def feast_walkthrough():
    limit,a,b=10,4,7
    @lru_cache(None)
    def best(f,used):
        choices=[f]
        choices.extend(best(f+x,used) for x in (a,b) if f+x<=limit)
        if not used:choices.append(best(f//2,True))
        return max(choices)
    assert best(0,False)==P.feast_cached(limit,a,b)==P.feast_table(limit,a,b)
    rows=[['stop at 3','no action',str(3)],
          ['eat 4',f'3 + 4 = {3+4}',f'best(7, True) = {best(7,True)}'],
          ['eat 7',f'3 + 7 = {3+7}',f'best(10, True) = {best(10,True)}']]
    return [
        'Follow one recursive question on limit 10 with fruit sizes 4 and 7: `best(7, False)`. Its input describes fullness 7 with the drink still unused. We want the greatest final fullness reachable from here, rather than the next fullness or a yes/no answer.',
        table(['Choice at fullness 7','Calculation','What the recursion does'],[
            ['stop','keep 7','candidate answer 7'],
            ['eat 4',f'7 + 4 = {7+4} > 10','reject this action; make no call'],
            ['eat 7',f'7 + 7 = {7+7} > 10','reject this action; make no call'],
            ['drink',f'7 // 2 = {7//2}','ask best(3, True); wait for its answer']]),
        'The drink leads to fullness 3 and marks the water used. Returning 3 immediately would stop the search too early: Bessie may still eat. Work out best(3, True) first. A second drink is not a candidate because True means the one drink has already been used.',
        table(['Choice after drinking','Immediate fullness','Candidate final fullness'],rows),
        f'At fullness 7 after drinking, neither fruit fits, so best(7, True) returns 7. At fullness 10 no fruit fits, so best(10, True) returns 10. The call at fullness 3 compares 3, 7 and 10 and returns {best(3,True)}. The waiting call best(7, False) now compares its stopping value 7 with that returned {best(3,True)}, and returns {best(7,False)}. Halving was an intermediate action; the returned answer includes the fruit eaten afterwards.'
    ]


def feast_flags():
    dry={0}
    for f in range(11):
        if f in dry:dry.update(f+x for x in (4,7) if f+x<=10)
    wet={f//2 for f in dry}
    for f in range(11):
        if f in wet:wet.update(f+x for x in (4,7) if f+x<=10)
    assert 7 in dry and 10 not in dry and 10 in wet
    return [
        'Pause over the change of question. We still use limit 10 and fruits 4 and 7. The recursive version asks what final fullness can be achieved from a situation. The iterative version will first discover which situations can be reached at all, then choose the largest reachable fullness at the end.',
        table(['Expression','Question it answers','Value in this example'],[
            ['best(7, False)','Starting at 7 with water unused, how full can Bessie eventually become?','10'],
            ['dry[7]','Can Bessie reach fullness 7 without drinking?','1: yes, eat one fruit of size 7'],
            ['dry[10]','Can Bessie reach fullness 10 without drinking?','0: no such sequence of fruits'],
            ['wet[10] after all passes','Can Bessie reach fullness 10 after drinking once?','1: yes, 0 to 7 to 3 to 10']]),
        'In `dry[7] = 1`, position 7 identifies the fullness and the value 1 means yes. It does not mean Bessie has fullness 1 or that exactly one route reaches 7. Likewise, `dry[10] = 0` means that fullness 10 is unreachable before water, not that the fullness has been reset to 0. The flags are evidence of legal routes; the final answer is an index whose flag is true.',
        'The three passes give these flags in a safe order: finish discovering all dry situations, place every possible water destination into the wet layer, then discover all further fruit moves in that layer. The following tables show each pass separately so that an entry reached by drinking is not mistaken for an entry reached by eating.'
    ]


def hps_walkthrough():
    john='HHSSP'
    def future(i,left,previous):
        scores=[]
        for s in product('HPS',repeat=len(john)-i):
            switches=sum(x!=y for x,y in zip((previous,)+s,s)) if previous else sum(x!=y for x,y in zip(s,s[1:]))
            if switches<=left:
                scores.append(sum(P.BEATS[x]==y for x,y in zip(s,john[i:])))
        return max(scores,default=0)
    rows=[]
    for g in 'HPS':
        change=int(g!='P');win=int(P.BEATS[g]==john[2]);later=future(3,1-change,g)
        rows.append([g,str(change),str(1-change),str(win),str(later),f'{win} + {later} = {win+later}'])
    assert future(0,1,'')==P.hps_cached(john,1)==P.hps_table(john,1)==4
    assert future(2,1,'P')==2
    return [
        'Use John\'s moves HHSSP and a budget of one switch. Suppose Bessie played P in rounds 0 and 1. She has won those two rounds, has used no switches, and is about to play round 2 against S. The recursive question is `best(2, 1, "P")`: next round 2, one switch left, previous gesture P.',
        'That call returns wins from rounds 2, 3 and 4 only. The two earlier wins are already earned and must not be included again inside every later call. Try each of the three gestures for round 2; then ask for the best score in the remaining rounds.',
        table(['Play now','Switch spent','Switches left','Win now','Wins later','Candidate'],rows),
        'For the H candidate, changing from P spends the remaining switch. H wins against S now. It must then stay H for the final S and P, winning against S and losing against P, so the remaining score is 1. This candidate contributes 1 + 1 = 2 future wins. The P and S candidates each contribute only 1; best(2, 1, "P") therefore returns 2.',
        table(['Part of the game','Round indices','Bessie / John','Wins'],[
            ['already played','0 and 1','PP / HH','1 + 1 = 2'],
            ['chosen continuation','2, 3 and 4','HHH / SSP','1 + 1 + 0 = 2'],
            ['whole strategy','0 through 4','PPHHH / HHSSP','2 + 2 = 4']]),
        'The table version below will record wins already earned and switches already used. The recursive version records switches still available and returns wins still to come. For a budget of one, used = 0 corresponds to left = 1, but their stored scores describe different parts of the game. Keep those two meanings separate when moving from the recursive program to the iterative one.'
    ]


def enrich(books):
    additions=[
        (1,'Use the target step as the cache key',1,cache_walkthrough()),
        (1,'Ask about the last jump to a stone',1,frog_walkthrough()),
        (2,'Fill totals in increasing order',1,dice_walkthrough()),
        (3,'Ask for the cheapest remaining cost',1,tower_walkthrough()),
        (3,'Count prefixes with a table',1,array_walkthrough()),
        (4,'A small recursive search',1,feast_walkthrough()),
        (4,'First pass: mark every fullness reachable before water',0,feast_flags()),
        (5,'A recursive view: choose the next gesture',1,hps_walkthrough()),
    ]
    for n,title,index,blocks in additions:
        matches=[s for ch in books[n]['chapters'] for s in ch['sections'] if s['title']==title]
        assert len(matches)==1,(n,title)
        matches[0]['blocks'][index:index]=blocks


if __name__=='__main__':
    for fn in (cache_walkthrough,frog_walkthrough,dice_walkthrough,tower_walkthrough,array_walkthrough,feast_walkthrough,feast_flags,hps_walkthrough):
        fn()
    print('PASS: eight detailed walkthroughs; computed examples agree with reference solutions.')
