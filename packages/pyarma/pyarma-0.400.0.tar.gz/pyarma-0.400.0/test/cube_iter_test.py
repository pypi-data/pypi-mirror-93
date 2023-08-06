from pyarma import *
c = cube(2,3,4,fill_randu)
c.print()
d = iter(c)
# Expected: print all c values.
for i in d:
    print(i)

print()
o = iterator(c, 1, 5)
# Expected: print elements 1 to 5(4?) only.
for i in o:
    print(i)
