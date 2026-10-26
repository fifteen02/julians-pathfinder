"""Independent counts, buffer wraparound, modulo and resource-shape checks."""
import ast,inspect
import programs as P
from dice_memory import ROWS,trace

# A forward distribution of counts, independent of the saved moving sum.
counts=[0]*501;counts[0]=1
for total in range(501):
    for face in range(1,7):
        if total+face<=500:counts[total+face]=(counts[total+face]+counts[total])%P.MOD
for n,want in enumerate(counts):
    assert P.dice_ring(n)==want and P.dice_window(n)==want
assert ROWS[5]['old_total']==0 and ROWS[5]['answer']==32
assert ROWS[6]['before']==[32,1,2,4,8,16]
assert ROWS[6]['after']==[32,63,2,4,8,16]
assert ROWS[6]['window']==125 and ROWS[6]['answer']==63
assert ROWS[7]['answer']==125
for r in trace(60):
    assert r['old_total']==r['total']-6
    assert r['slot']==r['total']%6
    assert len(r['after'])==6
    assert all(0<=v<P.MOD for v in r['after'])
    assert sorted(r['totals'])==list(range(r['total']-5,r['total']+1))
# Exercise modulo with a tiny modulus, where subtraction can be negative.
saved=P.MOD
try:
    P.MOD=7
    for n in range(40):assert P.dice_ring(n)==P.dice_table(n)==P.dice_window(n)
finally:P.MOD=saved
for n in (1000,1000000):assert P.dice_ring(n)==P.dice_window(n)==P.dice_table(n)
for name in ('dice_ring','dice_window'):
    tree=ast.parse(inspect.getsource(getattr(P,name)))
    lists=[node for node in ast.walk(tree) if isinstance(node,ast.List)]
    assert len(lists)==1 and ast.literal_eval(lists[0])==[0]
    assert '[0] * 6' in inspect.getsource(getattr(P,name))
print('PASS: Dice table/ring/window agree for totals 0-500, 1000 and 1000000; six-slot traces, wraparound, modulo and return timing checked.')
