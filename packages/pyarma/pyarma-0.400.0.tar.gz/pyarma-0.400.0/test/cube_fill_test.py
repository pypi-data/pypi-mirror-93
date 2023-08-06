from pyarma import *

m = m = cube(2,3,4,fill_ones)
m.print()

n = m = cube(2,3,4,fill_zeros)
n.print()

o = m = cube(2,3,4,fill_randu)
o.print()

q = m = cube(2,3,4,fill_randn)
q.print()

r = m = cube(2,3,4,fill_none)
r.print()