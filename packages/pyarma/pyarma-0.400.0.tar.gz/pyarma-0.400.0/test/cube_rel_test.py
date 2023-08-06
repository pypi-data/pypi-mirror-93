from pyarma import *

c = cube(2,3,4,fill_ones)
d = cube(2,3,4,fill_ones)

(c==d).print() # expected: all ones
(c!=d).print() # expected: all zeros
(c[0:1,0:1,0:1]==d[0:1,0:1,0:1]).print()
(c[0:1,0:1,0:1]!=d[0:1,0:1,0:1]).print()

c = cube(2,3,4,fill_randu)
d = cube(2,3,4,fill_randu)

c.print()
d.print()

(c>d).print()
(c<d).print()
(c[0:1,0:1,0:1]>d[0:1,0:1,0:1]).print()
(c[0:1,0:1,0:1]<d[0:1,0:1,0:1]).print()

(c>=d).print()
(c<=d).print()
(c[0:1,0:1,0:1]>=d[0:1,0:1,0:1]).print()
(c[0:1,0:1,0:1]<=d[0:1,0:1,0:1]).print()
