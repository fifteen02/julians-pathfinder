"""Student-facing context and working-space choices for the printed sheets."""
GUIDES = {
1: [
 ('Our route', 'Start with a brief recursion refresher; choose one warm-up exercise if you already know how calls stop. Then count staircase routes by hand. Write a recursive function, see which questions repeat, and save their answers. Then fill the same answers with a loop. Change the allowed jumps before trying Frog, where the answer is a minimum cost instead of a count.'),
 ('Recursion warm-up · L1-01 to L1-04', 'A function may call itself on a smaller input. The base case answers directly, without another call; every other call must move closer to the base case. A call that is waiting for a smaller call stays unfinished until that call returns its value.'),
 ('Staircase rules · L1-05 to L1-13', 'Start at ground level, called step 0. A move climbs exactly 1 or 2 steps. Count ordered lists of moves that land exactly on the target. For example, [1, 2] and [2, 1] are different routes. In L1-13 only, the permitted moves change to 1 or 3.'),
 ('Frog rules · L1-14 to L1-20', 'Number the stones 0, 1, 2 and so on. Start on stone 0 and finish on the last stone. A jump moves forward by one or two stone positions. Its cost is the absolute height difference: a jump from height 50 to height 30 costs 20. Add every jump cost in a route; find the smallest total.'),
 ('Names used in the questions', '`ways(n)` is a function returning the number of staircase routes to target step n. `ways[n]` is a list entry storing that count. Parentheses call a function; square brackets read a stored entry. In Frog, `heights[i]` is the height at stone position i, while `best[i]` is the cheapest total cost to reach it.'),
 ('What to complete in class', 'Complete both staircase and Frog: for each, follow the slow recursive solution, save repeated answers, then fill a table with a loop. The recursion warm-up is a short refresher; the remaining warm-up exercises can be used for extra practice. Explain each small example before running a large input.')],
2: [
 ('Our route', 'Count ordered dice sequences by their final number. Try recursion, save repeated answers, then fill a table. Then see how six reused entries reduce Dice memory from O(n) to O(1), with an optional running sum. Afterwards count grid paths by their final move. The full Dice table remains useful for learning; the buffer is a memory improvement.'),
 ('Dice rules · L2-02 to L2-08', 'Choose any finite ordered sequence of values from 1 to 6. Count sequences whose total is exactly the target n. There is no fixed number of throws and no probability calculation. [1, 2] and [2, 1] are different sequences. For L2-07 only, allow 1, 2 and 3.'),
 ('Large counts', 'The final iterative dice and grid programs return the remainder after dividing the count by 1,000,000,007. Python writes this as `count % 1_000_000_007`. Small examples on these sheets are below that number, so their counts are unchanged. L2-06 explains why taking remainders during the calculation is valid.'),
 ('Grid rules · L2-09 to L2-14', 'The grid has n rows and n columns, numbered from 0. A dot means an open cell; a star means a blocked cell. Start at row 0, column 0. Reach row n - 1, column n - 1 using moves of one cell right or one cell down. A path may never enter a blocked cell.'),
 ('Names used in the questions', '`ways[total]` stores the number of sequences whose sum is that total. `paths[r][c]` stores the number of paths to row r, column c. The indices identify a total or a cell; the stored values count sequences or paths. A recursive function answers the same question by asking about smaller totals or earlier cells.')],
3: [
 ('Our route', 'Ask what extra information changes the available choices. Tower needs the next player as well as the boss position. Array Description needs the neighbouring value as well as the position. Work a small case, describe the stored answer, then write recursion and a table.'),
 ('Tower rules · L3-01 to L3-06', 'Bosses are listed in order: 0 means easy and 1 means hard. Your friend starts. On each turn, the player must defeat the next one or two remaining bosses, then the other player moves. Your friend pays one point for each hard boss they defeat; you pay nothing. Both players cooperate to minimise the friend\'s total payment.'),
 ('Tower names', '`n` is the number of bosses. Position `i` identifies the next boss to defeat. `friend_turn` is True when your friend plays next and False when you play next. Position n means no bosses remain; it is just beyond the last valid list index.'),
 ('Array rules · L3-07 to L3-13', 'Fill every missing entry with an integer from 1 to m. A 0 in the input marks a missing entry; 0 is not allowed in the completed array. Keep fixed entries unchanged. Two neighbouring values may differ by at most 1. Count all valid completed arrays, returning the count modulo 1,000,000,007.'),
 ('Array names', '`n` is the number of entries and `m` is the largest allowed value. `i` is a position, starting at 0; `v` is a possible value placed there. A prefix through position i means the entries from position 0 up to and including position i. For example, the prefix through position 1 of [2, 3, 2] is [2, 3].')],
4: [
 ('Our route', 'First find all fullness values reachable without water. Next consider drinking from each of those values. Finally add fruit after the drink. Keep these three lists of results separate while tracing the example; they represent different moments in the calculation.'),
 ('Fruit Feast rules', 'The cow starts with fullness 0. There is unlimited fruit: one type adds a and the other adds b, both positive integers. Fullness must never exceed limit. A fruit that would exceed limit cannot be eaten. The cow may stop at any time; find the largest fullness she can reach.'),
 ('The one drink', 'Water is optional and can be used at most once, before, between or after eating. It changes fullness f to `f // 2`, where // rounds down. For example, 5 becomes 2. Fruit may be eaten afterwards, but a second drink is forbidden.'),
 ('Names used in the questions', '`dry[f]` says whether fullness f is reachable without having used water. `wet[f]` says whether it is reachable after using water. The position f is a fullness value. The entry is a yes/no flag, not a count of routes. Write Y for reachable and - for unreachable in the printed tables.'),
 ('Recursion and the table answer different questions', 'The recursive function returns the largest final fullness reachable from the current situation. The iterative tables store which situations can be reached from the start. Both must obey the same fruit and water rules. When tracing, always label which kind of answer you are recording.')],
5: [
 ('Our route', 'Count wins when one gesture is kept throughout. Then place one change by hand. To solve longer games, record the round, switches used and ending gesture. Compare keeping that gesture with changing it, and fill a fresh table for each round.'),
 ('Game rules', 'John\'s entire sequence is known in advance. Bessie chooses H (hoof), P (paper) or S (scissors) for each round. H beats S, S beats P, and P beats H. A win scores 1; a draw or loss scores 0. Maximise Bessie\'s total wins.'),
 ('Switch rules', 'The first gesture is free. A switch is a change of gesture between two consecutive rounds. The budget, called K in the judge\'s statement and budget in the code, allows at most that many changes, not exactly that many. For example, H, H, P uses one switch. Number rounds from 0, so round 2 is the third round.'),
 ('Names used in the questions', '`used` is the number of switches already used (written `used` in the code too). `g` is the current gesture. A score cell stores the most wins among strategies with that exact used and g after the specified round. Two different strategies may contribute to the same cell; keep the better score.'),
 ('Reading the tables', 'The columns headed H, P and S identify Bessie\'s ending gesture, not John\'s move. Write a dash for a state that is impossible. A score of 0 instead means a legal strategy exists but has no wins. L5-06 connects the dash to the program\'s negative-infinity value.')]
}

# These questions ask students to construct a program, not just explain a value.
# CODING is derived from IMPLEMENT below so the two cannot drift apart.

# Short written traces have labelled blank tables, rather than generic lines alone.
TABLES = {
 'L4-09': (['Fullness f','0','1','2','3','4','5','6','7','8','9'], [['dry[f]','Y','','','','','','','','',''],['just drank','','','','','','','','','',''],['wet[f]','','','','','','','','','','']]),
 'L2-13': (['Test grid','Your prediction','Program output'], [["['.']  (one open cell)",'',''],["['*']  (one blocked cell)",'',''],["['..', '..']  (open 2 by 2)",'',''],["['...', '.*.', '...']  (centre blocked)",'','']]),
 'L1-01': (['Call','Prints','Calls next'], [['countdown(3)','',''],['','',''],['','',''],['','','']]),
 'L1-02': (['Call','Waits for','Returns'], [['sum_squares(4)','',''],['sum_squares(3)','',''],['sum_squares(2)','',''],['sum_squares(1)','',''],['sum_squares(0)','nothing','0']]),
 'L1-05': (['Step','1','2','3','4','5'], [['Routes','','','','','']]),
 'L1-13': (['Step','0','1','2','3','4','5','6','7'], [['ways[step]','1','','','','','','','']]),
 'L1-19': (['Stone i','0','1','2','3'], [['heights[i]','10','30','20','40'],['best[i]','0','','','']]),
 'L2-07': (['Total','0','1','2','3','4','5'], [['ways[total]','1','','','','','']]),
 'L3-12': (['Position','Given','v = 1','v = 2','v = 3'], [['0','0','','',''],['1','0','','',''],['2','3','','','']]),
 'L4-07': (['Fullness f','0','1','2','3','4','5','6','7','8','9','10'], [['wet[f]','','','','','','','','','','','']]),
 'L5-12': (['John prefix','Switches used','Ending gesture','Stored score'], [['','','','']]),
}

TABLE_ANSWERS = {
 'L1-01': [['countdown(3)','3','countdown(2)'],['countdown(2)','2','countdown(1)'],['countdown(1)','1','countdown(0)'],['countdown(0)','Go!','nothing']],
 'L1-02': [['sum_squares(4)','sum_squares(3)','16 + 14 = 30'],['sum_squares(3)','sum_squares(2)','9 + 5 = 14'],['sum_squares(2)','sum_squares(1)','4 + 1 = 5'],['sum_squares(1)','sum_squares(0)','1 + 0 = 1'],['sum_squares(0)','nothing','0']],
 'L1-05': [['Routes','1','2','3','5','8']],
 'L1-13': [['ways[step]','1','1','1','2','3','4','6','9']],
 'L1-19': [['heights[i]','10','30','20','40'],['best[i]','0','20','10','30']],
 'L2-07': [['ways[total]','1','1','2','4','7','13']],
 'L2-13': [["['.']  (one open cell)",'1','1'],["['*']  (one blocked cell)",'0','0'],["['..', '..']  (open 2 by 2)",'2','2'],["['...', '.*.', '...']  (centre blocked)",'2','2']],
 'L3-12': [['0','0','1','1','1'],['1','0','2','3','2'],['2','3','0','0','5']],
 'L4-07': [['wet[f]','Y','-','Y','Y','Y','-','Y','Y','Y','Y','Y']],
 'L4-09': [['dry[f]','Y','-','-','-','Y','-','Y','-','Y','-'],['just drank','Y','-','Y','Y','Y','-','-','-','-','-'],['wet[f]','Y','-','Y','Y','Y','-','Y','Y','Y','Y']],
 'L5-12': [['HHS','1','H','3']],
}

PARTS = {
1: [(1,4,'Warm-up: functions that call themselves'),(5,13,'Staircase: count, remember, then loop'),(14,20,'Frog: compare complete route costs'),(21,21,'Extension: recover a cheapest Frog route')],
2: [(1,7,'Dice: count ordered sequences'),(8,8,'Optional: reuse six counts'),(9,14,'Grid Paths: count routes to each cell')],
3: [(1,6,'Tower: remember whose turn comes next'),(7,13,'Arrays: remember the neighbouring value')],
4: [(1,4,'Understand the fruit and water choices'),(5,8,'Build the three passes'),(9,11,'Test and explain the pass order')],
5: [(1,4,'Plan gestures and count switches'),(5,9,'Store scores and compare continuations'),(10,12,'Test the budget and explain the state')]
}

def part(lesson, index):
    return next(title for a,b,title in PARTS[lesson] if a <= index <= b)

# Every question that asks students to implement something: the functions to
# start from (their signatures are printed exactly as in solutions.py, nested
# functions included) and 1-3 hints that guide without giving the answer.
IMPLEMENT = {
 'L1-03': (['power2'], ['Trace the inputs until they pass 0. Where should the chain stop?', 'Check your repaired function on the stopping input before trying 3.']),
 'L1-04': (['factorial'], ['What is the smallest n you can answer directly?', 'If you already knew factorial(n - 1), what single step would give factorial(n)?']),
 'L1-08': (['stairs_slow'], ['Which targets can you answer without a smaller call? Think about 0 and about negative targets.', 'The last move is 1 or 2 steps. Which smaller targets do those leave?']),
 'L1-12': (['stairs_table'], ['How long must the list be so that ways[n] exists?', 'Which entry do you know before the loop starts?', 'When you fill ways[step], which entries must already be filled?']),
 'L1-13': (['stairs_13'], ['Which line of stairs_table depends on the allowed jumps?', 'A jump can only start from a step that exists. What must be true before you read an earlier entry?']),
 'L1-16': (['frog_slow'], ['What is the smallest i you can answer directly?', 'Which earlier stones can the last jump into stone i start from?', 'What does cost(i) need to know about each of those stones?']),
 'L1-18': (['frog_table'], ['What is best[0], before any jump?', 'Which earlier entries does best[i] need, and are they filled when the loop reaches i?']),
 'L1-21': (['frog_path'], ['When a candidate becomes the cheapest, what earlier stone should you remember?', 'Start at the last stone and follow the saved indices. How will you recognise the start?', 'In which order did you collect the stones, and which order should you return?']),
 'L2-04': (['dice_slow', 'dice_cached'], ['What is the count for total 0?', 'Which faces can be the last one when the remaining total is small?', 'What input identifies a repeated question, and where must the saved answers live so that every call shares them?']),
 'L2-05': (['dice_table'], ['Which entry is known before the loop?', 'For each total, which earlier totals can the last face come from?', 'Where do you take the remainder so that stored numbers stay small?']),
 'L2-07': (['dice_123'], ['Which part of dice_table depends on the faces allowed?', 'Check total 4 by hand before you run the code.']),
 'L2-11': (['grid_cached'], ['Which cells can you answer directly: outside the grid, blocked, and the start?', 'From which two cells can the last move into (r, c) come?']),
 'L2-12': (['grid_table'], ['Create the table so that every row is a separate list.', 'In which order must you visit the cells so that the cells above and to the left are already filled?', 'What does a blocked cell store?']),
 'L3-04': (['tower_cached'], ['What is the remaining cost when no bosses remain?', 'On one turn, how many bosses can the player take, and who pays for them?', 'After the turn, who plays next, and from which position?']),
 'L3-06': (['tower_table'], ['Which positions are filled before the loop?', 'In which direction must i move so that positions i + 1 and i + 2 are ready?', 'Which entry is the answer, given that your friend starts?']),
 'L3-09': (['array_cached'], ['What does count return when every position has been filled?', 'Which values may position i take if the input fixes it?', 'How does the previous value restrict the next value?']),
 'L3-12': (['array_rolling'], ['What does the first row look like, when there is no previous value?', 'Which entries of the previous row can lead to value v?', 'Why must the new row be built separately from the old row?']),
 'L4-04': (['feast_cached'], ['Stopping is always allowed. What does that give as a first answer?', 'Which moves are legal from (fullness, used_water)?', 'Which move changes used_water, and can it happen twice?']),
 'L4-08': (['feast_table'], ['Which fullness is reachable before anything is eaten?', 'Keep the three passes in order: eat, drink once, eat again.', 'Which array does each pass read, and which does it write?']),
 'L5-05': (['hps_cached'], ['What does best return when no rounds remain?', 'When does choosing a gesture cost a switch, and when is it free?', 'Which choices are not allowed with the switches left?']),
 'L5-09': (['hps_table'], ['What are the scores after round 0, and which states are impossible then?', 'For a new cell, which cells of before lead to it by staying, and which by switching?', 'What should an impossible state hold so that max ignores it?']),
}

# Derive the new arithmetic traces from the teaching functions.
from recursion_intro import return_rows
TABLE_ANSWERS['L1-02'] = return_rows('sum_squares',4,'+')

# A later testing task reuses the earlier implementation, without a new scaffold.
CODING = set(IMPLEMENT)
REUSE = {
 'L1-19': ('frog_table', 'L1-18'),
 'L2-13': ('grid_table', 'L2-12'),
 'L4-09': ('feast_table', 'L4-08'),
 'L4-10': ('feast_table', 'L4-08'),
 'L5-10': ('hps_table', 'L5-09'),
 'L5-11': ('hps_table', 'L5-09'),
}
