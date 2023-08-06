from pyarma import *

m = mat(2,3,fill_ones)
m.print()

n = mat(2,3,fill_zeros)
n.print()

o = mat(2,3,fill_randu)
o.print()

p = mat(3,3,fill_eye)
p.print()

q = mat(2,3,fill_randn)
q.print()

r = mat(2,3,fill_none)
r.print()