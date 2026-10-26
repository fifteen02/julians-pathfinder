"""Standalone worked answers, kept in worksheet order and in the course style."""
from pathlib import Path
import concurrent.futures
import json
import build_course as B
from content import LESSONS
from compile_all import compile_one
from sheet_guidance import TABLES, TABLE_ANSWERS, part

EXPLANATIONS = {
'L1-06': 'Each route to step 5 has exactly one last move. Removing that move leaves a route to step 4 or step 3. These two groups include every route, and no route is in both groups, so adding the counts neither misses nor repeats a route.',
'L1-08': 'Each line of the trace shows one call and its returned count. Indentation identifies the calls it makes. Repeated lines are separate calls, not reused answers.',
'L1-09': 'The two displayed ways(3) calls both calculate ways(2) and ways(1), and those calls branch again. The two ways(2) calls also repeat work. A saved answer lets a later call with the same input return immediately.',
'L1-11': 'For example, the first call for target n can wait for n - 1, which waits for n - 2. Those calls remain on the stack together. A cache reduces how often an answer is computed; a loop also removes this chain of waiting calls.',
'L1-12': 'The index is a step number; the stored value counts routes. Start with one empty route at step 0. At step 1 there is no predecessor step -1 in the table, so read only step 0. From step 2 onwards, both predecessors exist.',
'L1-15': 'At stone 2, greedy pays 10 to reach stone 3 instead of 20 to reach stone 4. However, it then pays 30 to reach height 10. The alternative pays 20 now and 0 on the final jump: 10 + 20 + 0 = 30.',
'L1-16': 'For stone 2 in the six-stone example, the route through stone 1 costs 30 + abs(30 - 50) = 50. The direct jump from stone 0 costs 0 + abs(30 - 20) = 10. The minimum is 10. Both candidates include the complete earlier route cost.',
'L1-18': 'For the last stone, coming from stone 4 costs 30 + abs(10 - 10) = 30. Coming from stone 3 costs 20 + abs(10 - 40) = 50. Store 30. Do not add every entry in best: each entry already measures a complete route from stone 0.',
'L1-19': 'For stone 3, coming from stone 2 costs 10 + abs(40 - 20) = 30. Coming from stone 1 costs 20 + abs(40 - 30) = 30 as well. Thus 0, 1, 3 is another cheapest route. The large test below uses iteration only.',
'L1-20': 'ways[step] counts routes to that step. best[i] is the cheapest complete cost to stone i. Staircase includes both last-move groups; Frog chooses the cheaper of the two last-jump totals.',
'L2-03': 'For target 4, a final 1 leaves target 3 with 4 sequences; a final 2 leaves target 2 with 2; a final 3 leaves target 1 with 1; a final 4 leaves target 0 with 1. A final 5 or 6 is impossible. Total 5 adds 8 + 4 + 2 + 1 + 1 = 16; total 6 adds 16 + 8 + 4 + 2 + 1 + 1 = 32.',
'L2-04': 'These implementations skip faces larger than the remaining target, so they never make a negative-target call. The uncached trace below includes every call for target 4. The cached version stores the result for each target; later calls with the same target read it instead of rebuilding the branch.',
'L2-08': 'The old group contains totals 1, 2, 3, 4, 5, 6. The next group contains totals 2, 3, 4, 5, 6, 7. Only two entries change: discard the count for total 1, and include the count for total 7. In the optional circular-buffer implementation, physical slot order is different from this chronological order.',
'L2-09': 'The first route visits cells (0,0), (0,1), (0,2), (1,2), (2,2). The second visits (0,0), (1,0), (2,0), (2,1), (2,2). In each pair, the first number is the row and the second is the column. Neither route visits (1,1).',
'L2-10': 'The open start stores 1 for the empty path. At row 1, column 2, the cell above contributes 1 and the blocked cell to the left contributes 0: 1 + 0 = 1. At the bottom right, above and left contribute 1 each, giving 2.',
'L2-12': 'For the incorrect construction, bad = [[0] * 2] * 2 repeats references to one row. After bad[0][0] = 1, the grid is [[1, 0], [1, 0]]. A comprehension instead creates two rows, so the same assignment gives [[1, 0], [0, 0]].',
'L2-14': 'A dice sequence has one final face, even when earlier faces repeat. A nonempty grid path has one final move: right or down. Removing that last choice gives the earlier sequence or path counted by the recurrence. The empty sequence and the open starting cell are handled by the base answer 1.',
'L3-04': 'For [1, 0, 1, 1] at position 0, taking one boss costs 1 + cost(1, False) = 1 + 1 = 2. Taking two costs 1 + 0 + cost(2, False) = 1. The second choice is better. Both players minimise the same total payment.',
'L3-05': 'First set both entries at position 4 to 0: there are no bosses left. At position 3, your friend must pay 1, while you pay 0. At position 2, your friend can take one hard boss and leave the last to you, costing 1. You can take both and leave no payment, costing 0.',
'L3-08': 'If the new value is 2, the neighbour rule permits 1, 2 and 3 immediately before it. A fixed input value of 1 removes the other new-value choices entirely. Their counts are zero because they violate the fixed entry, even if a predecessor count exists.',
'L3-10': 'At position 2, ending in value 2 accepts all three previous ending values, so its count is 1 + 1 + 1 = 3. At position 3 the fixed value is 1; only previous values 1 and 2 can precede it, giving 2 + 3 = 5.',
'L3-12': 'The first missing entry allows each of 1, 2 and 3 once. The next row becomes [2, 3, 2]. The last entry is fixed to 3, so its count is the previous count ending in 2 plus the previous count ending in 3: 3 + 2 = 5. For [1, 3], the difference is 2, so the neighbour rule fails.',
'L4-03': 'For example, from fullness 4 with water unused, drinking can move to fullness 2. From fullness 4 with water already used, that move is illegal. A single flag would hide whether this next action is allowed.',
'L4-04': 'Stopping returns the current fullness f, so the cow is never forced to make another move. Eating keeps the water status unchanged. Drinking changes the status from unused to used, even at fullness 0; it cannot create a cycle back to an unused-water state.',
'L4-07': 'Starting from the immediate-after-water values 0, 2, 3 and 4: 0 can reach 4, 7 and 8; 2 can reach 6, 9 and 10; 3 can reach 7 and 10; 4 can reach 8. Include the starting values too because eating no further fruit is allowed.',
'L4-09': 'The final row also keeps every value in the just-drank row. From fullness 2, further fruit reaches 6 or 8. From fullness 3, it reaches 7 or 9. No continuation reaches fullness 5, so that entry remains unmarked.',
'L4-11': 'During a single increasing-fullness scan, fullness 3 would be visited before fullness 7. If drinking from 7 marks 3 only afterwards, that scan will not return to 3 to discover 10. Completing the drink pass before the final fruit pass makes all such starting values available in time.',
'L5-04': 'Suppose the next selected gesture is H. A history already ending with H spends no switch; a history ending with P spends one. Therefore even equal scores and equal usage are not enough to merge those two histories.',
'L5-06': 'A switch needs a gap between two rounds. After the first round there is no such gap yet. Keeping H against John\'s H is legal and scores 0, whereas using exactly one switch is impossible. Those are different situations.',
'L5-07': 'The new zero-switch row is [1, 2, 0]. For exactly one switch: ending H gives max(1, 2, 0) + 1 = 3; ending P gives max(1, 0, 0) + 0 = 1; ending S gives max(1, 0, 2) + 0 = 2. Each maximum compares staying with the same gesture after one switch, or switching now from another gesture after zero switches.',
'L5-08': 'The table records the best score for each exact usage and ending gesture after each prefix of John\'s sequence. The final maximum is max(2, 2, 1, 4, 2, 3) = 4. A strategy attaining it is P, P, H, H, H.',
'L5-09': 'For each new round, all candidate scores must come from the completed previous round. Reading a cell already updated for the current round could reuse this round\'s score or spend another switch in the same gap. A fresh now table keeps the two rounds separate.',
}
EXTRA_CODE = {'L1-19':['frog_table'], 'L2-13':['grid_table'], 'L3-06':['tower_table']}
RUNS = {
'L2-11': "print(grid_cached(['...', '.*.', '...']))",
'L1-19': "print(frog_table([10, 30, 20, 40]))\nprint(frog_table([7] * 100000))",
'L2-13': "for grid in [['.'], ['*'], ['..', '..'], ['...', '.*.', '...']]:\n    print(grid_table(grid))",
'L3-06': "for bosses in [[0], [1], [1, 1, 1]]:\n    print(tower_table(bosses))",
}

def trace(n, jumps, name):
    def count(k):
        if k < 0: return 0
        if k == 0: return 1
        return sum(count(k-j) for j in jumps if name == 'ways' or j <= k)
    lines=[]
    def visit(k, prefix='', branch=''):
        lines.append(prefix+branch+f'{name}({k}) -> {count(k)}')
        if k <= 0: return
        children=[k-j for j in jumps if name == 'ways' or j <= k]
        for i,ch in enumerate(children):
            visit(ch,prefix+('    ' if branch == '`-- ' else '|   ' if branch else ''),'`-- ' if i==len(children)-1 else '|-- ')
    visit(n)
    return '\n'.join(lines)

# Questions follow on. Each block is typeset into a box first: if it fits in
# 60% of a page it is placed whole (so it moves to the next page rather than
# split); a longer block is released so it can start on the current page and
# break only between its own parts (answer, each program). A part is kept
# whole whenever it fits on one page.
FLOW = r"""\makeatletter
\newsavebox{\qbox}
\newenvironment{qblock}[1][0.6]{\def\qlimit{#1}\par\setbox\qbox\vbox\bgroup\hsize\linewidth\color@begingroup}{\par\color@endgroup\egroup
  \ifdim\dimexpr\ht\qbox+\dp\qbox\relax>\qlimit\textheight\relax\unvbox\qbox\else\box\qbox\fi\par}
\makeatother
\newcommand{\qtopic}[2]{{\color{quiet}\fontsize{9}{12}\selectfont\textbf{#1}}\par{\heavy\fontsize{19}{23}\selectfont\raggedright #2\par}\vspace{5pt}}
"""

def render(L):
    cover=B.cover(L,'teacher').replace('TEACHER GUIDE','WORKSHEET ANSWERS').replace('Teaching prompts and worked answers.','Worked answers, tables and complete code.').replace(r'Ask a question, give students time to think,\\then work through the answer together.',r'Check each answer against your own working.\\Follow the question IDs from the worksheet.').replace(r'Understand what each step establishes\\and why it leads to the next.',r'Questions appear in worksheet order.\\Alternative correct solutions are welcome.')
    s=B.bookhead(L,'worksheet answers').replace(r'\begin{document}',FLOW+r'\begin{document}',1)+cover+B.reference(L)
    s+=r'\textbf{Using these answers.} Each question and its supplied diagram or table appear before the answer. Completed tables, and answer diagrams where the question has one, follow the worked answer. The IDs match the worksheet; answer pages have their own page numbers. Each program is printed in full once, with imports, line numbers and a small check; a later question that uses the same program names the page where it appears and gives its own check.'+(' An optional question remains optional here.' if any(u['extension'] for u in L['units']) else '')+r'\par\bigskip{\color{lightink}\hrule height .4pt}\bigskip'
    shown={}
    for i,u in enumerate(L['units'],1):
        # One block per question: the written answer, then one sub-block per
        # program. A block that fits on a page is never split (see FLOW).
        s+=r'\par\markboth{'+B.tex(u['title'])+r'}{}\begin{qblock}\begin{qblock}[0.95]'+'\n'
        s+=r'\qtopic{'+u['id']+(' / OPTIONAL EXTENSION' if u['extension'] else '')+r'}{'+B.tex(u['title'])+'}\n'
        s+=r'{\small\color{quiet}'+B.tex(part(L['n'],i))+r'}\par\medskip'+'\n'
        s+=r'\textbf{Question.} '+B.tex(u['q'])+'\n\n'
        if u.get('given'): s+=r'\textbf{Code supplied with the question.}'+B.listing(B.given_code(u))
        if u['id'] in B.IMPLEMENT: s+=B.SP.print_tex(u['id'],B.tex)
        # Reproduce the material supplied with the worksheet question before
        # revealing any answer. Blank tables are part of the question too.
        question_d=u.get('diagram')
        if u['id'] in TABLES:
            h,rows=TABLES[u['id']]
            question_d=dict(kind='table',head=h,rows=rows)
        if question_d and question_d['kind'] in ('table','tree','lastmove'):
            label='Table supplied with the question.' if question_d['kind']=='table' else 'Diagram supplied with the question.'
            s+=r'\textbf{'+label+r'}\par'+B.diagram(question_d,True)+'\n'
        s+=r'\par\medskip\textbf{Worked answer.} '+B.tex(u['a'])+'\n\n'
        d=u.get('answer_diagram') or u.get('diagram')
        if u['id'] in TABLES:
            d=dict(kind='table',head=TABLES[u['id']][0],rows=TABLE_ANSWERS[u['id']])
        # An unchanged input table has already been supplied above. A filled
        # or annotated visual belongs here, after the written answer.
        if d and (d['kind']!='table' or d.get('blank') or u['id'] in TABLES or u.get('answer_diagram')):
            label='Completed table.' if d['kind']=='table' else 'Diagram for the answer.'
            visual=B.diagram(d)
            if d['kind']=='tree':
                for key in ('e','f'):
                    visual=visual.replace(r'\node[box,fill=paper] ('+key+')',r'\node[box,fill=wash] ('+key+')')
            s+=r'\textbf{'+label+r'}\par'+visual+'\n'
        if u['id']=='L1-21': s+=r'\par\smallskip\resizebox{\linewidth}{!}{'+B.FG.tikz(True)+r'}\par '+B.tex('Solid arrows show the returned route. The dashed arrows are other legal jumps. Arrow costs add to 10 + 20 + 0 = 30.')+'\n'
        if u['id'] in EXPLANATIONS: s+=B.tex(EXPLANATIONS[u['id']])+'\n\n'
        if u['id'] in ('L1-08','L2-04'):
            t=trace(3,(1,2),'stairs_slow') if u['id']=='L1-08' else trace(4,tuple(range(1,7)),'dice_slow')
            s+=r'\textbf{Complete call trace.} Each arrow gives the returned count.'+B.listing(t).replace(r'\begin{lstlisting}',r'\begin{lstlisting}[language={}]')
        s+=r'\end{qblock}'+'\n'
        fns=EXTRA_CODE.get(u['id'],B.codes(u))
        # The question asks for the cached grid version; the uncached alternative
        # belongs in the tutor book, not in this answer.
        if u['id']=='L2-11': fns=['grid_cached']
        for j,fn in enumerate(fns):
            code=B.precode(fn)
            s+=r'\begin{qblock}[0.95]'+'\n'
            if fn in shown:
                # Already printed in full: name it and give this question's check.
                s+=r'\medskip\textbf{Same implementation as '+shown[fn]+r'} (\texttt{'+B.esc(fn)+r'}, page~\pageref{ans-'+fn+r'}).\par'
                run=RUNS.get(u['id'],u.get('run'))
                s+=r'\textbf{Check.} Run this after that function.'+B.listing(run)
                s+=r'\textbf{Expected output.}'+B.listing(B.example_output(run)).replace(r'\begin{lstlisting}',r'\begin{lstlisting}[language={}]')
                s+=r'\end{qblock}'+'\n'
                continue
            shown[fn]=u['id']
            s+=r'\medskip\textbf{One complete Python implementation: '+B.tex(fn)+r'.}\label{ans-'+fn+r'}\par'+B.numbered(code)
            run=RUNS.get(u['id'],u.get('run'))
            if run:
                if len(fns)>1:
                    # Existing shared examples sometimes name both versions;
                    # keep this page independently runnable.
                    run=f"print({fn}(4))" if u['id']=='L2-04' else (f"print({fn}(0), {fn}(6), {fn}(7), {fn}(8))" if u['id']=='L2-08' else run)
                output=B.example_output(run)
                s+=r'\textbf{Check.} Run this after the function above.'+B.listing(run)
                s+=r'\textbf{Expected output.}'+B.listing(output).replace(r'\begin{lstlisting}',r'\begin{lstlisting}[language={}]')
            if fn in B.RECURSIVE: s+=r'\textbf{Recursion depth.} '+B.tex(B.RECURSION_NOTE.split(': ',1)[1])+'\n\n'
            s+=r'\end{qblock}'+'\n'
        s+=r'\end{qblock}\par\medskip{\color{lightink}\hrule height .4pt}\bigskip'+'\n'
    return s+r'\end{document}'

def build():
    for L in LESSONS:
        (B.ROOT/f'Lesson {L["n"]}/worksheet_answers.tex').write_text(render(L))

if __name__=='__main__':
    build()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        report=list(pool.map(compile_one,[(n,'worksheet_answers') for n in range(1,6)]))
    Path('answers-compile-report.json').write_text(json.dumps(report,indent=2))
    for item in report: print(json.dumps(item))
    assert all(x['ok'] and not x['warnings'] for x in report), 'Resolve compilation warnings before publishing.'
