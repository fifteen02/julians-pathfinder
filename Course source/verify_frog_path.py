"""Independently enumerate tiny routes and check large returned paths."""
from itertools import product
from programs import frog_path, frog_table
from frog_path_extension import HEIGHTS, trace
from frog_graph import EDGES

def all_costs(h,i=0):
    if i==len(h)-1:return [0]
    return [abs(h[j]-h[i])+tail for j in (i+1,i+2) if j<len(h) for tail in all_costs(h,j)]

def check(h,expected):
    value,path=frog_path(h)
    assert value==expected,(h,value,expected)
    assert path[0]==0 and path[-1]==len(h)-1
    assert all(isinstance(i,int) and 0<=i<len(h) for i in path)
    assert all(b-a in (1,2) for a,b in zip(path,path[1:]))
    assert sum(abs(h[b]-h[a]) for a,b in zip(path,path[1:]))==value

count=0
for n in range(1,8):
    for h in product((0,1,3),repeat=n):check(h,min(all_costs(h)));count+=1
assert frog_path(HEIGHTS)==(30,[0,2,4,5])
assert trace(HEIGHTS)[1]==[-1,0,0,2,2,4]
assert frog_path([10,30,20,40])==(30,[0,2,3])
assert frog_path([7,7,7])==(0,[0,1,2])
assert EDGES==[(0,1,30),(0,2,10),(1,2,20),(1,3,10),(2,3,10),(2,4,20),(3,4,30),(3,5,30),(4,5,0)]
for n in (500,100000):
    h=[(i*7919)%10000 for i in range(n)];check(h,frog_table(h))
print(f'PASS: {count} exhaustively checked inputs; ties, graph labels, 500 and 100000 stones; every returned path legal and optimal.')
