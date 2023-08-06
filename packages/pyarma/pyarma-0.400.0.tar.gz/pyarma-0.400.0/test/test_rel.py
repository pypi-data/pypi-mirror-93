from pyarma import *

m = mat(2,3,fill_ones)
n = mat(2,3,fill_ones)
o = umat([1,3,5])
p = m[o]
q = n[o]

(m==n).print() # expected: all ones
(m!=n).print() # expected: all zeros
(p==q).print() # expected: all ones
(p!=q).print() # expected: all zeros
(m[0:1,0:1]==n[0:1,0:1]).print()
(m[0:1,0:1]!=n[0:1,0:1]).print()
(m[diag]==n[diag]).print()
(m[diag]!=n[diag]).print()

m = mat(2,3,fill_randu)
n = mat(2,3,fill_randu)

m.print()
n.print()

(m>n).print()
(m<n).print()
(m[0:1,0:1]>n[0:1,0:1]).print()
(m[0:1,0:1]<n[0:1,0:1]).print()
(m[diag]>n[diag]).print()
(m[diag]<n[diag]).print()

(m>=n).print()
(m<=n).print()
(m[0:1,0:1]>=n[0:1,0:1]).print()
(m[0:1,0:1]<=n[0:1,0:1]).print()
(m[diag]>=n[diag]).print()
(m[diag]<=n[diag]).print()