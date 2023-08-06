from pyarma import *

m = mat(2,3,fill_randu)
n = mat(1,3,fill_randu)
o = mat()

m.print()

print(any(m)) # expected: rowvec of 111
print(any(any(m))) # exp: 1
print(any(n)) # expected: umat of 1
print(any(o)) # expected: umat of 0
print(any(m > 0.5)) # expected: rowvec, if greater than .5, 1

print(all(m)) # exp: 111
print(all(all(m))) # exp: 1
print(all(n)) # exp: 1
print(all(o)) # exp: 1
print(all(m > 0.5)) # expected: rowvec, if greater than .5, 1

prod(m).print()
prod(n).print()
prod(o).print()