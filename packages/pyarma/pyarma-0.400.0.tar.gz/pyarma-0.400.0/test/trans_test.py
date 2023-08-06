from pyarma import *

m = mat(2,3,fill_randu)

m.print()

m.t().print()
m[:,:].t().print()
m[diag].t().print()

m.st().print()
m[:,:].st().print()
m[diag].st().print()

trans(m).print()
trans(m[:,:]).print()
trans(m[diag]).print()

strans(m).print()
strans(m[:,:]).print()
strans(m[diag]).print()