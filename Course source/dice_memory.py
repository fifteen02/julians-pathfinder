"""Teach the six-slot dice buffer before the running-sum optimisation."""
import programs as P
from book_blocks import chapter,section,table,figure,code,python,cost


def trace(n):
    recent=[0]*6;recent[0]=1
    totals=[0,-5,-4,-3,-2,-1];window=1;rows=[]
    for total in range(1,n+1):
        slot=total%6;oldest=recent[slot];old_total=totals[slot];answer=window
        before=recent.copy();before_totals=totals.copy()
        recent[slot]=answer;totals[slot]=total
        window=(window-oldest+answer)%P.MOD
        assert answer==P.dice_table(total) and window==sum(recent)%P.MOD
        rows.append(dict(total=total,slot=slot,oldest=oldest,old_total=old_total,answer=answer,window=window,
                         before=before,after=recent.copy(),before_totals=before_totals,totals=totals.copy()))
    return rows

ROWS=trace(9)
INTRO='The full table keeps a count for every total from 0 to n. To calculate the count for total 7, however, we only read counts for totals 1 to 6. To calculate total 8, we only read totals 2 to 7. Once total 7 is saved, the count for total 1 will never be read again. We can reuse its storage.'
NAMES='Keep six entries in a list named recent. A slot is an index into that list: 0, 1, 2, 3, 4 or 5. A total is the target sum of the dice; a count is the number of ordered sequences for that total. These are three different numbers. The count for total t is stored in slot t % 6. The remainder wraps the chosen index back to 0 after slot 5. The list entries do not move.'
INIT='Initially recent is [1, 0, 0, 0, 0, 0]. The 1 counts the empty sequence for total 0. The other five entries stand for impossible negative totals, whose counts are 0. These zeros let the same six-entry calculation work when total is smaller than 6. For n = 0 the loop does not run, and slot 0 correctly returns 1.'
SUM='The circular buffer alone saves memory. Summing six entries still takes a fixed amount of work per total. We can also save their sum in window. Before an iteration, window is the answer we are about to store. After storing that answer, subtract the overwritten count and add the new count to prepare the next sum.'
END='After total 7, recent[1] holds 63, the requested answer. The updated window is 125, ready for total 8. Return recent[n % 6], not window. Assigning an integer to a list entry saves that value; changing window later does not change the saved entry.'


def slot_table():
    r=ROWS[6]
    return ['Slot']+list(map(str,range(6))),[
        ['Total before 7']+list(map(str,r['before_totals'])),
        ['Count before 7']+list(map(str,r['before'])),
        ['Total after 7']+list(map(str,r['totals'])),
        ['Count after 7']+list(map(str,r['after']))]


def ring_picture():
    r=ROWS[6]
    s=r'\begin{tikzpicture}[x=1cm,y=1cm,>=Stealth,every node/.style={font=\small,align=center}]'+'\n'
    for i in range(6):
        s+=rf'\node[draw=ink,fill={"codepaper" if i==1 else "white"},minimum width=16mm,minimum height=15mm] (s{i}) at ({i*2},0) {{slot {i}\\count {r["before"][i]}}};'
        s+=rf'\node[below=3mm] at (s{i}.south) {{total {r["before_totals"][i]}}};'
        if i:s+=rf'\draw[->] (s{i-1})--(s{i});'
    s+=r'\draw[->] (s5.north) -- ++(0,0.65) -| node[pos=.25,above] {the next slot after 5 is 0} (s0.north);'
    s+=r'\node[below=14mm] at (s1.south) {next write: total 7 uses slot 1};'
    return s+r'\end{tikzpicture}'


def apply(lesson,make_table):
    u=next(u for u in lesson['units'] if u['id']=='L2-08')
    u.update(title='Extension: six slots instead of a full table',
        q='Before total 7, recent is [32, 1, 2, 4, 8, 16] in slots 0 to 5. These store counts for totals [6, 1, 2, 3, 4, 5]. The running sum window is 63. Which slot does 7 % 6 choose, and which old count must be saved before overwriting it? Store the answer for total 7, then prepare the next sum. What should dice_window(7) return? Explain why six slots are enough.',
        a='7 % 6 chooses slot 1. Save its old count 1, then store 63. Prepare the next sum: 63 - 1 + 63 = 125, for total 8. Return recent[1] = 63. Only the six preceding counts are needed: reusing their slots reduces memory from O(n) to O(1). Time remains O(n).',
        notes=INTRO+'\n\n'+NAMES+'\n\n'+INIT+'\n\n'+SUM+'\n\n'+END+'\n\nUse dice_ring first to separate saving memory from saving additions. Both versions use O(n) time and O(1) extra memory. With n = 1,000,000, recent still has only six entries. MOD keeps stored counts bounded. The 5-minute slot in the timetable is a preview; allow 15-20 minutes as follow-up for the whole trace and code.',
        hint='Separate the total, its slot and the count stored there. Save the old count, write the current answer, then prepare the next sum.',
        mis='Slot 1 can hold the count for total 1 or total 7 at different times. The updated running sum answers the next total.',
        code=['dice_ring','dice_window'],run='print(dice_ring(7), dice_window(7))\nprint(dice_ring(8), dice_window(8))')
    head,rows=slot_table();u['answer_diagram']=make_table(head,rows)


def book_chapter():
    head,rows=slot_table()
    return chapter('Dice: reduce memory to six saved counts','Reuse an answer after its last contribution, then maintain the sum of the saved counts.',
      section('Why the whole table is unnecessary',['L2-08'],'Identify exactly which counts each new total reads before discarding any value.','Use fixed slots without moving the entries.',
        INTRO,table(['Next total','Earlier totals read','Counts added','Answer'],[
          [str(t),' to '.join(map(str,(t-6,t-1))),' + '.join(str(P.dice_table(i)) for i in range(t-6,t)),str(P.dice_table(t))] for t in (7,8,9)]),
        'For target 1,000,000, dice_table allocates 1,000,001 entries. Every iteration still reads at most six counts. Keeping only the six useful counts reduces storage to six entries, regardless of the target. We are discarding values that no future iteration can use; we are not skipping any contribution to the current answer.'),
      section('Reuse six slots in a circle',['L2-08'],'Distinguish a target total, a list slot and the count stored in that slot.','Keep the sum as well as the six entries.',
        NAMES,table(['Target total','Slot calculation'],[[str(t),f'{t} % 6 = {t%6}'] for t in range(4,10)]),
        INIT,
        'For the diagram, use the buffer just before total 7: recent = [32, 1, 2, 4, 8, 16]. Slot 0 holds the count 32 for total 6. Slot 1 still holds the count 1 for total 1. The target totals are no longer in left-to-right order in the list, but each count is still present.',
        figure(ring_picture(),'The arrows show the order in which slots are reused, not a movement of the stored counts. A circular buffer is an ordinary fixed-size list whose chosen index wraps around.'),
        'First sum all six entries and save the result in answer. Only then overwrite the selected slot. At total 6, the count for total 0 is still needed to count the single throw [6]; it can be discarded only after computing that answer. At total 7, the count for total 1 makes its final contribution.',
        code('dice_ring','print(dice_ring(0), dice_ring(6), dice_ring(7), dice_ring(8))'),
        python(['sum','mod'],'read the six counts before overwriting',
          '`sum(recent)` adds the six stored counts. `% MOD` keeps the count modulo 1,000,000,007. `total % 6` instead chooses a list slot from 0 to 5. These uses of % have different jobs. `answer` saves the sum before `recent[total % 6] = answer` overwrites one of its inputs.'),
        'dice_ring already uses O(1) extra memory. Its loop runs n times and adds six entries each time, so the time is O(6n), written O(n). The next version keeps the sum between iterations to avoid repeating those six additions.'),
      section('Save the sum and prepare the next answer',['L2-08'],'Update the running sum in the right order and return the answer for n.','Move to Grid Paths, where each count belongs to a cell.',
        SUM,
        table(['Action for total 7','Calculation or value','Meaning'],[
          ['Choose the slot','7 % 6 = 1','the physical list index'],
          ['Save the old count','oldest = recent[1] = 1','count for total 1'],
          ['Write the answer','recent[1] = 63','count for total 7'],
          ['Prepare the next sum','63 - 1 + 63 = 125','count for total 8']]),
        table(head,rows),END,
        'The count for total 1 was included in the sum that produced 63. It is removed only when preparing the next sum. Reading oldest after overwriting the slot would read 63 instead of 1, so we must save it first.',
        code('dice_window','print(dice_window(0), dice_window(6), dice_window(7), dice_window(8))'),
        python(['mod'],'keep both stored counts and the running sum bounded',
          '`window` starts at 1. Each update takes `% MOD`, so the value stored by `recent[slot] = window` is already a remainder. It does not need another % on that assignment. Python also handles a negative intermediate difference with a positive modulus: the final remainder stays between 0 and MOD - 1.'),
        table(['Total','Slot','Old count','Answer stored','Next running sum'],[
          [str(r['total']),str(r['slot']),str(r['oldest']),str(r['answer']),f"{r['answer']} - {r['oldest']} + {r['answer']} = {r['window']}"] for r in ROWS],
          r'>{\raggedright\arraybackslash}p{10mm}>{\raggedright\arraybackslash}p{10mm}>{\raggedright\arraybackslash}p{19mm}>{\raggedright\arraybackslash}p{25mm}X'),
        'The trace starts with window = 1 and recent = [1, 0, 0, 0, 0, 0]. The first five overwritten entries are zeros for impossible negative totals. At total 6 the overwritten entry is the starting count 1; at total 7 it is the count 1 for total 1. The equal values have different meanings.',
        cost('Cost of dice_window, line by line','dice_window',((9,),dict(n=9),'For n = 9'),(dict(n=1000000),'For n = 1,000,000'),[
          ('recent = [0] * 6','allocate six entries once',lambda n:1),
          ('slot = total % 6','choose one slot per total',lambda n:n),
          ('oldest = recent[slot]','read one old count per total',lambda n:n),
          ('recent[slot] = window','write one count per total',lambda n:n),
          ('window = (window - oldest + recent[slot]) % MOD','one subtraction, addition and remainder per total',lambda n:n)]),
        table(['Version','Time','Extra memory','What changes'],[
          ['dice_table','O(n)','O(n)','keeps every count'],['dice_ring','O(n)','O(1)','keeps six counts; adds them each time'],['dice_window','O(n)','O(1)','also keeps their sum']]),
        'Both six-slot versions return the same remainder as the full table. MOD bounds the stored integers, and the number of list entries stays six. There is no recursion stack. The saving is memory; keeping the running sum also reduces the fixed work per iteration. It does not change the linear time bound.'
      ))


def markdown():
    r=ROWS[6]
    head,rows=slot_table()
    tab=' | '.join(head)+'\n'+' | '.join(['---']*len(head))+'\n'+'\n'.join(' | '.join(row) for row in rows)
    return '**Worked explanation: read after attempting L2-08.**\n\n### Why six entries are enough\n\n'+INTRO+'\n\n'+NAMES+'\n\n'+INIT+'\n\n'+tab+'\n\n'+SUM+'\n\nAt total 7: save old count 1, store 63, then prepare 63 - 1 + 63 = 125.\n\n'+END+'\n\n`dice_ring` sums six values per iteration; `dice_window` updates their saved sum. Both take O(n) time and O(1) extra memory. Here `window` is the same running sum as `sum_contributions` in the circular-buffer version.'


def slides(start,end,stxt,number,tex,ruled):
    data=[
      ('QUESTION','Which earlier answers can we forget?','To count sequences for total 7, the last face is 1 to 6. Which earlier totals do we read? For total 8, which count stops being needed?',None),
      ('ANSWER','Only six earlier counts are needed','Total 7 reads counts for totals 1 to 6. Total 8 reads totals 2 to 7. After computing total 7, the count for total 1 can be overwritten. Six reused entries give O(1) memory; we still compute n answers, taking O(n) time.',(['Next total','Reads totals','Counts added','Answer'],[['7','1 to 6','1 + 2 + 4 + 8 + 16 + 32','63'],['8','2 to 7','2 + 4 + 8 + 16 + 32 + 63','125']])),
      ('QUESTION','A total is not a slot','Six slots are numbered 0 to 5. Store a count in slot total % 6. Which slots do totals 5, 6, 7 and 8 use? What must happen before replacing an old count?',None),
      ('ANSWER','The index wraps; the values stay put','Totals 5, 6, 7 and 8 use slots 5, 0, 1 and 2. Read all six counts to form the current answer before overwriting a slot. The same slot holds different totals at different times.',(['Total','Slot calculation'],[[str(t),f'{t} % 6 = {t%6}'] for t in range(5,9)]))]
    s=''
    for phase,title,body,tab in data:
        s+=start+'\n'+stxt(1.5,16.9,29,13,r'\heavy LESSON 2 / L2-08 / BUFFER / '+phase,'quiet')+number()+stxt(1.5,15.4,29,34,r'\heavy '+tex(title))
        s+=stxt(1.5,12.4,29,24,tex(body),'ink','body')
        if tab:s+=r'\node[anchor=north west,inner sep=0,text width=29cm] at ([yshift=-8mm]body.south west) {'+ruled(tab[0],tab[1],tex,True)+r'};'+'\n'
        s+=end+'\n'
    return s
