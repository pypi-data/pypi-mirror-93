from pyarma import *
import math

# Test instantiation
c = cube(3,3,3,fill_randu)

# Test print
c.print()

# Test min
print(c.min())

# Test max
print(c.max())

# Test index_min
print(c.index_min())

# Test index_max
print(c.index_max())
 
# Generate empty matrix
p = cube()

# Test is_empty
print(c.is_empty()) # False
print(p.is_empty()) # True

# Generate matrix with inf
q = cube(2,3,4,fill_randu)
q[0,0,0] = math.inf

# Test is_finite
print(c.is_finite()) # True
print(q.is_finite()) # False

# Test has_inf
print(c.has_inf()) # False
print(q.has_inf()) # True

# Generate matrix with nan
s = cube(2,3,4,fill_randu)
s[0,0,0] = math.nan

# Test has_nan
print(c.has_nan()) # False
print(s.has_nan()) # True

# Testing submatrix safety (keep_alive<0,1>)
b = cube(2,3,4,fill_randu)
c = b[0:1, 0:1, 0:1]
b.print()
c.print()
b = 5 # Underlying matrix would have been destroyed here
c.print() # This would have accessed garbage/caused a segfault

# Testing submatrix setters
a = cube(3,4,5,fill_randu)
a.print()
# Didn't work properly
# a[0:2,0:2,0:2].ones()
# a.print()
# a[0:2,0:2,0:2].zeros()
# a.print()
# a[0:2,0:2,0:2].randn()
# a.print()
# a[0:2,0:2,0:2].randu()
# a.print()
# a[0:2,0:2,0:2].fill(4.2)
# a.print()
# a[0:2,0:2,0:2].clean(5)
a.print()
a[0:2,0:2,0:2].replace(0, 6.9)
a.print()
# Setting row
a[1,:,:] = cube(1,4,5,fill_ones)
# Setting col
a[:,1,:] = cube(3,1,5,fill_ones)
a.print()

# Testing submatrix safety (keep_alive<0,1>)
d = a
d.fill(5)
a.print()
d.print()
a = 5 # Underlying matrix would have been destroyed here
d.print() # This would have accessed garbage/caused a segfault

# Testing ops (same types)
tora = cube(3,3,3,fill_randu)
dora = cube(3,3,3,fill_ones)
tora.print()
result = tora + dora 
result.print() # expected: added by 1
result = tora - dora
result.print() # expected: negatives
result = tora @ dora
result.print() # expected: same
result = tora / dora
result.print() # expected: same
result = tora * dora
result.print() # expected: normal matmul

print("testing subview-subview ops\d")
# Testing ops (subview-subview)
takasu = cube(3,3,3,fill_randu)
aisaka = cube(3,3,3,fill_ones)
tora = takasu[:,:,:]
dora = aisaka[:,:,:]
tora.print()
result = tora + dora 
result.print() # expected: added by 1
result = tora - dora
result.print() # expected: negatives
result = tora @ dora
result.print() # expected: same
result = tora / dora
result.print() # expected: same
result = tora * dora
result.print() # expected: normal matmul

print("Now testing broadcasts\d")

# Testing broadcasts
kitamura = cube(1,3,3,fill_ones)
tora.print()
(tora+kitamura).print()
(kitamura+tora).print() # should be +1
kitamura = cube(3,1,3,fill_ones)
(tora+kitamura).print()
(kitamura+tora).print() # should be +1

# Testing in-place broadcasts
kitamura = cube(1,3,3,fill_ones)
tora += kitamura
tora.print()
tora -= kitamura
tora.print()

# Testing subview broadcasts
kushieda = tora[:,:,:]
# (kushieda+kitamura).print()
(kitamura+kushieda).print()

print("now testing inplaces\d")

# Testing in-place ops (same types)
tora += dora
tora.print() # +1
tora -= dora
tora.print() # nrm
dora.fill(2)
dora.print()
tora @= dora
tora.print() # x2
tora /= dora
tora.print() # nrm
tora *= dora
tora.print() # matmul

print("now testing cube-subv ops\d")

# # Subview tests
# print(c)
# x = cube(2,2,fill_ones)
# print(x)
# # Calls __radd__
# y = c[0:1, 0:1, 0:1] + x # Expected: 2x2 submatrix of c + 1
# y.print()
# # Calls __iadd__ and __radd__
# x += c[0:1, 0:1, 0:1]
# x.print()
# # __add__
# x.ones()
# a1 = x + c[0:1, 0:1, 0:1]
# a1.print()
# # __sub__
# # __isub__
# # __mul__
# # __imul__
# # __truediv__
# # __idiv__
# # __matmul__
# # __imatmul__

# Testing ops (cube-subv)
tora = cube(3,3,3,fill_randu)
ryuji = cube(3,3,3,fill_ones)
dora = ryuji[:,:,:]
tora.print()
result = tora + dora 
result.print() # expected: added by 1
result = tora - dora
result.print() # expected: negatives
result = tora @ dora
result.print() # expected: same
result = tora / dora
result.print() # expected: same
result = tora * dora
result.print() # expected: normal matmul

print("testing subv-cube ops\d")

# Testing ops (subv-cube)
tora = cube(3,3,3,fill_randu)
ryuji = cube(3,3,3,fill_ones)
dora = ryuji[:,:,:]
tora.print()
result = dora + tora
result.print() # expected: added by 1
result = dora - tora
result.print() # expected: negatives
result = dora @ tora
result.print() # expected: same
result = dora / tora
result.print()
result = dora * tora
result.print() # expected: normal matmul

print("now testing subv-diagv\d")
# Testing subv-diagv ops (B/C)
tora = cube(3,3,3,fill_randu)
ryuji = cube(3,3,3,fill_ones)
dora = tora[:,:,:] # subv of all of tora
takasu = ryuji[diag] # diagonal of ones
dora.print()
result = dora + takasu
result.print() # expected: added by 1
result = dora - takasu
result.print() # expected: negatives
result = dora @ takasu
result.print() # expected: same
result = dora / takasu
result.print()
result = dora * takasu
result.print() # expected: normal matmul

print("now testing subv-diagv, no B/C\d")
# Testing subv-diagv ops
tora = cube(3,1,fill_randu)
ryuji = cube(3,3,3,fill_ones)
dora = tora[:,:,:] # subv of all of tora
takasu = ryuji[diag] # diagonal of ones
dora.print()
result = dora + takasu
result.print() # expected: added by 1
result = dora - takasu
result.print() # expected: negatives
result = dora @ takasu
result.print() # expected: same
result = dora / takasu
result.print()
# result = dora * takasu
# result.print() # expected: normal matmul

# Testing in-place ops (cube-subv)

print("now testing diagv ops")

# Testing ops (cube-diagv)
aisaka = cube(3,1,fill_randu) # random vector
takasu = ryuji[diag] # diag of ones
aisaka.print()
takasu.print()
result = aisaka + takasu 
result.print() # expected: added by 1
result = aisaka - takasu
result.print() # expected: negatives
result = aisaka @ takasu
result.print() # expected: same
result = aisaka / takasu
result.print() # expected: same
minori = cube(1,3,fill_randu) # matmul can only be done with NxM * MxN
result = aisaka * minori
result.print() # expected: normal matmul

# Testing in-place ops (cube-diagv)

# Testing diagv broadcast
aisaka = cube(3,3,3,fill_randu) # random vector
takasu = ryuji[diag] # diag of ones
aisaka.print()
takasu.print()
result = aisaka + takasu 
result.print() # expected: added by 1
result = aisaka - takasu
result.print() # expected: negatives
result = aisaka @ takasu
result.print() # expected: same
result = aisaka / takasu
result.print() # expected: same

print("testing diagv-diagv\d")
# Testing diagv-diagv
tenori = aisaka[diag]
tenori.print()
takasu.print()
(tenori + takasu).print()
(takasu-tenori).print()
(tenori @ takasu).print()
(tenori / takasu).print()
(tenori * takasu.as_row()).print()

print("testing diagv-cube\d")

# Testing ops (diagv-cube, B/C)
aisaka = cube(3,3,3,fill_randu) # random vector
takasu = ryuji[diag] # diag of ones
aisaka.print()
takasu.print()
result = takasu + aisaka
result.print() # expected: added by 1
result = takasu - aisaka
result.print() # expected: negatives
result = takasu @ aisaka
result.print() # expected: same
result = takasu / aisaka
result.print() # expected: same
result = aisaka * takasu
result.print() # expected: normal matmul

# Testing diagv-subv
print("now testing diagv-subv\d")
# Testing subv-diagv ops
tora = cube(3,3,3,fill_randu)
ryuji = cube(3,3,3,fill_ones)
dora = tora[:,:,:] # subv of all of tora
takasu = ryuji[diag] # diagonal of ones
dora.print()
result = takasu + dora
result.print() # expected: added by 1
result = takasu - dora
result.print() # expected: negatives
result = takasu @ dora
result.print() # expected: same
result = takasu / dora
result.print()

print("now testing scalars")
# Testing scalar ops
tora += 1
tora.print()
(tora+1).print()
tora -= 1
tora.print()
(tora-1).print()
tora *= 2
tora.print()
(tora*2).print()
tora /= 2
tora.print()
(tora/2).print()

print("now testing scalars on subviews")
# Testing scalar ops
dora += 1
dora.print()
(dora+1).print()
dora -= 1
dora.print()
(dora-1).print()
dora *= 2
dora.print()
(dora*2).print()
dora /= 2
dora.print()
(dora/2).print()

print("now testing scalars on diags")
# Testing scalar ops
takasu += 1
takasu.print()
(takasu+1).print()
takasu -= 1
takasu.print()
(takasu-1).print()
takasu *= 2
takasu.print()
(takasu*2).print()
takasu /= 2
takasu.print()
(takasu/2).print()

# testing Terry's problem
(1-cube(1,2,fill_zeros)).print()
(1+cube(1,2,fill_zeros)).print()
(2*cube(1,2,fill_ones)).print()