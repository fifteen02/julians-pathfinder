"""Frog route reconstruction, shared by the classroom and detailed tutorial."""
import programs as P
from book_blocks import section, table, figure, code, python

HEIGHTS=[20,50,30,40,10,10]


def trace(heights):
    best=[0]*len(heights);previous=[-1]*len(heights);rows=[]
    rows.append(['0',str(heights[0]),'start: cost 0','no earlier stone','0','-1: stop'])
    for i in range(1,len(heights)):
        one=best[i-1]+abs(heights[i]-heights[i-1])
        best[i]=one;previous[i]=i-1
        two=None
        if i>=2:
            two=best[i-2]+abs(heights[i]-heights[i-2])
            if two<one:best[i]=two;previous[i]=i-2
        rows.append([str(i),str(heights[i]),f'{best[i-1]} + {abs(heights[i]-heights[i-1])} = {one}',
                     'not available' if two is None else f'{best[i-2]} + {abs(heights[i]-heights[i-2])} = {two}',
                     str(best[i]),str(previous[i])])
    path=[];back=[];i=len(heights)-1
    while i!=-1:
        path.append(i)
        back.append([str(i),str(path),str(previous[i]) if previous[i]!=-1 else '-1: stop'])
        i=previous[i]
    path.reverse()
    assert (best[-1],path)==P.frog_path(heights)
    return best,previous,rows,back,path


def add_classroom(lesson,unit,make_table):
    best,previous,_,_,path=trace(HEIGHTS)
    u=unit('Frog: recover a cheapest path',
        'Extend your cost solution: write frog_path(heights), returning (cost, path), where path lists stone indices from start to finish. For heights [20, 50, 30, 40, 10, 10], record in previous[i] which earlier stone gives best[i]. Use -1 for the start. On equal costs keep i - 1. Trace backwards from the last stone, then return the path in forward order.',
        f'The previous list is {previous}. Starting at stone 5, follow 5, 4, 2, 0, then stop at -1. Reverse the collected list to get {path}. The function returns (30, {path}): the jump costs are 10 + 20 + 0 = 30.',
        'Teach this after the minimum-cost solution is secure. Allow another 15-20 minutes as an extension or follow-up; keep the two-hour core route unchanged. First fill best and previous together. best[i] is a cost, while previous[i] is a stone index. A pointer can skip a stone. Save the predecessor only when its candidate becomes the chosen best cost.\n\nTrace backwards without making any new greedy decisions: the choices were recorded while comparing whole-route costs. Stop before reading previous[-1], because Python would interpret -1 as the last list entry. Reverse once after collecting the indices. A tie may produce several cheapest routes; our strict comparison keeps i - 1, and the checks use that convention.\n\nThis is a classroom extension: the original AtCoder problem still asks for the cost alone. Both filling the table and recovering a route are linear in the number of stones. Do not copy a complete route into every table cell; that can make total copying quadratic.',
        'Save a stone index beside each chosen cost. Follow those saved indices from the finish until the start marker.',
        'previous[i] holds an index, not a height or a cost. A cheapest path need not be unique or use the fewest jumps.',
        code='frog_path',run='print(frog_path([20, 50, 30, 40, 10, 10]))',extension=True,
        answer_diagram=make_table(['Stone i']+list(map(str,range(len(HEIGHTS)))),[
            ['heights[i]']+list(map(str,HEIGHTS)),['best[i]']+list(map(str,best)),['previous[i]']+list(map(str,previous))]))
    u['id']='L1-21';lesson['units'].append(u)
    lesson['exercises'].append(dict(id='L1-21',function='frog_path',signature='heights',solution='frog_path',
        tests=[('([20, 50, 30, 40, 10, 10],)',(30,path)),('([10, 30, 20, 40],)',P.frog_path([10,30,20,40])),('([7, 7, 7],)',P.frog_path([7,7,7])),('([7],)',P.frog_path([7]))]))


def tutorial_section():
    best,previous,rows,back,path=trace(HEIGHTS)
    import frog_graph as FG
    picture=r'''\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,every node/.style={font=\small,align=center}]
\foreach \id/\x/\h in {0/0/20,2/3/30,4/6/10,5/9/10}
 {\node[draw=ink,fill=codepaper,minimum width=17mm,minimum height=12mm] (s\id) at (\x,0) {stone \id\\height \h};}
\draw[->] (s0.north) to[bend left=35] node[above] {cost 10} (s2.north);
\draw[->] (s2.north) to[bend left=35] node[above] {cost 20} (s4.north);
\draw[->] (s4.north) to[bend left=35] node[above] {cost 0} (s5.north);
\draw[->,dashed] (s5.south) to[bend left=35] node[below] {previous[5] = 4} (s4.south);
\draw[->,dashed] (s4.south) to[bend left=35] node[below] {previous[4] = 2} (s2.south);
\draw[->,dashed] (s2.south) to[bend left=35] node[below] {previous[2] = 0} (s0.south);
\end{tikzpicture}'''
    tie=P.frog_path([10,30,20,40])
    return section('Extend the answer: recover a cheapest path',['L1-21'],
        'Return the minimum cost together with one route that achieves it, and distinguish costs from saved stone indices.',
        'Check the original cost-only problem and its judge format.',
        'The cost program answers how much the cheapest route costs. We now also want to show which stones the frog visits. Use the same six heights [20, 50, 30, 40, 10, 10], at positions 0 through 5. This is an extension after the cost solution; the original problem still requires only the cost.',
        figure(FG.tikz(True),'The same graph of legal jumps, now with one cheapest route drawn in solid arrows. Other legal arrows are dashed. The total along the solid arrows is 10 + 20 + 0 = 30.'),
        'We already compare the candidate routes when we fill best[i]. At that exact moment, save which earlier stone supplied the chosen candidate. Call this new list previous: previous[i] is the index of the stone immediately before i on the route we chose. It can be i - 1 or i - 2. It is not necessarily the adjacent stone in the input.',
        table(['Stone','Height','From i - 1','From i - 2','best[i]','previous[i]'],rows,
              r'>{\raggedright\arraybackslash}p{10mm}>{\raggedright\arraybackslash}p{12mm}XX>{\raggedright\arraybackslash}p{16mm}>{\raggedright\arraybackslash}p{20mm}'),
        'At stone 4, the chosen total is 30 via stone 2, so save best[4] = 30 and previous[4] = 2 together. The 30 measures effort; the 2 identifies a stone. At stone 5, the cheaper route comes from stone 4, so previous[5] = 4. These saved choices explain how to attain each recorded cost.',
        'Stone 0 is the start, so it has no predecessor. Store -1 there as a stop marker. This -1 is not a stone to visit and is not an instruction to read the last entry of a Python list. The backwards loop checks the marker before indexing again.',
        'To recover the final route, start at the last stone, position 5. Append its index to a list, read its saved predecessor, and repeat. Do not choose a cheaper-looking jump at this stage: the forwards cost calculation already chose a predecessor using the complete earlier cost.',
        table(['Current stone','Indices collected so far','Next saved index'],back),
        f'The collected indices run from finish to start: {list(reversed(path))}. Reversing their order gives {path}. Reversing the list does not make the frog jump backwards; it changes how we present the already chosen forward route.',
        figure(picture,'Solid arrows show the returned forward route. Dashed arrows show how the program follows saved predecessors from the finish to recover that same route.'),
        table(['Returned jump','Heights','Cost'],[[f'{a} to {b}',f'{HEIGHTS[a]} to {HEIGHTS[b]}',f'abs({HEIGHTS[b]} - {HEIGHTS[a]}) = {abs(HEIGHTS[b]-HEIGHTS[a])}'] for a,b in zip(path,path[1:])]),
        f'The costs add to {" + ".join(str(abs(HEIGHTS[b]-HEIGHTS[a])) for a,b in zip(path,path[1:]))} = {best[-1]}, agreeing with best[5]. Every jump advances by one or two positions, so the returned list is a legal route as well as a witness to the minimum cost.',
        'Ties do not require remembering every route. Initialise each stone from i - 1, then change to i - 2 only when that candidate is strictly cheaper. For heights [10, 30, 20, 40], the two final candidates both cost 30. This convention keeps predecessor 2 and returns '+str(tie)+'. The route [0, 1, 3] has the same cost, but this program returns just one cheapest route. It does not promise the fewest jumps.',
        code('frog_path','print(frog_path([20, 50, 30, 40, 10, 10]))'),
        python(['append','reverse','tuple','while','neq'],'collect, reverse and return two results',
               '`path.append(i)` adds the current stone index at the end of the list. `while i != -1:` repeats while there is a real stone to process. After appending, `i = previous[i]` moves to its saved predecessor. `path.reverse()` reverses the list in place and returns None, so do not assign its result back to path. `return best[-1], path` returns a pair, called a tuple. The caller can write `cost, path = frog_path(heights)` to receive the two results separately.'),
        table(['Work','How much','Why'],[
            ['fill best and previous','n - 1 iterations','at most two candidates per stone'],
            ['follow previous','at most n iterations','each saved index is smaller; the chain reaches stone 0'],
            ['reverse the collected list','at most n entries','one reversal after the backwards walk'],
            ['storage','three lists, each at most n entries','costs, predecessors and the returned path']]),
        'Here n is the number of stones. These loops run one after another, so their costs add: O(n) time overall and O(n) memory, as for the full cost table. Saving a complete copied path at every stone would be different: with a one-step route, the copies would contain 1 + 2 + ... + n entries. Saving one predecessor per stone avoids that quadratic amount of copying.',
        'In class, first ask for the previous list and the backwards trace, then ask students to write frog_path. Use L1-21 as a 15-20 minute extension or follow-up after the two-hour core lesson. The notebook and local frog-path tests include a single stone, ties, equal heights and larger inputs.')
