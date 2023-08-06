from pyarma import *
m = mat(2,3,fill_randu)
m.print()
n = iter(m)
# Expected: print all m values.
for i in n:
    print(i)

print()
o = iterator(m, 1, 5)
# Expected: print elements 1 to 4 only.
for i in o:
    print(i)

print()
p = col_iter(m)
# Expected: print first col only
for i in p:
    print(i)

print()
q = col_iter(m, 1, 2)
# Expected: print second and third only
for i in q:
    print(i)