"""One weighted Frog graph, reused in print, slides and notebooks."""
import base64
from frog_path_extension import HEIGHTS, trace
from book_blocks import figure, table

EDGES=[(i,j,abs(HEIGHTS[j]-HEIGHTS[i])) for i in range(len(HEIGHTS)) for j in (i+1,i+2) if j<len(HEIGHTS)]
INTRO='Use heights [20, 50, 30, 40, 10, 10], at stone indices 0 to 5. Draw one circle for each stone and an arrow for every allowed jump: one or two positions forwards. A diagram of positions connected by arrows is a graph. The circles are its nodes; the arrows are its edges. Label each arrow with the absolute height difference, which is the cost of that jump.'
LINK='This has the same forward connections as the staircase with moves of one or two steps. Staircase counts all routes. Frog attaches a cost to each arrow and asks for a route whose total cost is smallest. The horizontal position is the stone index, not its height; a fall in height still costs energy.'
DIFFERENCE='The graph has one node per stone. A recursion tree shows calls: several branches may ask for the cheapest cost to stone 2. Those calls refer to the same graph node. Caching merges their repeated work. Iteration visits nodes from left to right: every incoming arrow then comes from a stone whose best cost is already known.'


def tikz(highlight=False):
    chosen=set(zip(trace(HEIGHTS)[4],trace(HEIGHTS)[4][1:])) if highlight else set()
    s=r'\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,every node/.style={font=\small}]'+'\n'
    for i,h in enumerate(HEIGHTS):
        s+=rf'\node[draw=ink,circle,minimum size=8mm,fill=codepaper] (g{i}) at ({i*2},0) {{{i}}};'+'\n'
        s+=rf'\node[below=3mm] at (g{i}.south) {{height {h}}};'+'\n'
    for i,j,c in EDGES:
        style='very thick,draw=ink' if (i,j) in chosen else ('draw=quiet,dashed' if highlight else 'draw=ink')
        if j==i+1:
            s+=rf'\draw[->,{style}] (g{i}.east) -- node[above,fill=white,inner sep=2pt] {{{c}}} (g{j}.west);'+'\n'
        else:
            s+=rf'\draw[->,{style}] (g{i}.north) to[bend left=45] node[above,fill=white,inner sep=2pt] {{{c}}} (g{j}.north);'+'\n'
    return s+r'\end{tikzpicture}'


def book_blocks():
    return [INTRO,figure(tikz(),'Every arrow is a legal jump. Arrow labels are jump costs; circle labels are stone indices.'),LINK,
        'For this preview, suppose we know the cheapest cost to stone 2 is 10 and the cheapest cost to stone 3 is 20. The worked route table that follows will derive those earlier costs. To reach stone 4, add the cost of its incoming arrow to each earlier total.',
        table(['Arrow into stone 4','Earlier route cost','Last jump cost','Whole cost to stone 4'],[
            ['3 to 4','20','abs(10 - 40) = 30','20 + 30 = 50'],
            ['2 to 4','10','abs(10 - 30) = 20','10 + 20 = 30']]),
        'The table previews the decision at stone 4. Once the earlier costs are known, the route through stone 2 is cheaper: 30 rather than 50. The next calculation must compare whole costs, not just arrow labels. We will now turn that decision into a recursive function.',DIFFERENCE]


def svg(highlight=False):
    chosen=set(zip(trace(HEIGHTS)[4],trace(HEIGHTS)[4][1:])) if highlight else set()
    s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 250"><rect width="900" height="250" fill="white"/><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#555"/></marker></defs><g font-family="sans-serif" text-anchor="middle" fill="#252525">'
    for i,j,c in EDGES:
        x=70+150*i;y=70+150*j
        path=f'M{x+22},155 L{y-26},155' if j==i+1 else f'M{x},130 C{x+50},15 {y-50},15 {y},130'
        dash=' stroke-dasharray="6 5"' if highlight and (i,j) not in chosen else ''
        s+=f'<path d="{path}" fill="none" stroke="#333" stroke-width="{4 if (i,j) in chosen else 1.6}" marker-end="url(#arrow)"{dash}/>'
        s+=f'<text x="{(x+y)/2}" y="{144 if j==i+1 else 43}" font-size="19">{c}</text>'
    for i,h in enumerate(HEIGHTS):
        x=70+150*i
        s+=f'<circle cx="{x}" cy="155" r="23" fill="#f6f6f4" stroke="#333"/><text x="{x}" y="162" font-size="22">{i}</text><text x="{x}" y="210" font-size="18">height {h}</text>'
    return s+'</g></svg>'


def notebook_cell(mdcell,highlight=False):
    intro=(INTRO+'\n\n'+LINK+'\n\n'+DIFFERENCE if not highlight else 'Follow the solid arrows: 0 → 2 → 4 → 5. Their costs add to 10 + 20 + 0 = 30. Dashed arrows remain legal, but are not on this returned route. The saved predecessor indices recover the solid arrows backwards; reversing the collected indices presents the forward route.')
    c=mdcell('### '+('One cheapest path through the graph' if highlight else 'Frog as a graph, like the staircase')+'\n\n'+intro+'\n\n![Frog graph: stone indices, heights and jump costs](attachment:frog-graph.svg)')
    c['attachments']={'frog-graph.svg':{'image/svg+xml':base64.b64encode(svg(highlight).encode()).decode()}}
    return c


def slides(start,end,stxt,number,tex,highlight=False):
    modes=[('ANSWER / PATH','Follow the recorded choices', 'The solid arrows are 0 to 2, 2 to 4 and 4 to 5. Total cost: 10 + 20 + 0 = 30. Dashed arrows are legal alternatives.\n\nprevious[5] = 4, previous[4] = 2, previous[2] = 0. Trace 5, 4, 2, 0, then reverse the list.')] if highlight else [
        ('GRAPH / QUESTION','The same connections as the stairs','Circles show stone indices; arrows show legal jumps and their costs.\n\nWhich arrows enter stone 4? What must we know before choosing the cheapest route into it?'),
        ('GRAPH / ANSWER','Compare complete costs into a stone','Suppose the cheapest costs to stones 3 and 2 are already known: 20 and 10. To stone 4 via stone 3: 20 + 30 = 50. Via stone 2: 10 + 20 = 30. Choose 30.\n\nStairs adds route counts. Frog takes the smaller total cost. One graph node represents a stone; the recursion tree may ask for that stone repeatedly.')]
    out=''
    for mode,title,body in modes:
        out+=start+'\n'+stxt(1.5,16.9,29,13,r'\heavy LESSON 1 / '+('L1-21' if highlight else 'FROG / L1-16')+' / '+mode,'quiet')+number()
        out+=stxt(1.5,15.4,29,34,r'\heavy '+tex(title))
        out+=stxt(1.5,13.4,29,20,tex('Data: heights [20, 50, 30, 40, 10, 10]. Stone indices run from 0 to 5.'))
        out+=r'\node[anchor=north west,inner sep=0] at (3,11.8) {\resizebox{25cm}{!}{'+tikz(highlight)+r'}};'+'\n'
        out+=stxt(1.5,5.6,29,21,tex(body))+end+'\n'
    return out
