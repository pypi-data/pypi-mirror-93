from pyarma import *

# Cube class
A = cube(5, 5, 5, fill_randu)
# x = A[1,2,3]
# x = 2

B = A + A
C = A @ B
D = A / B

X = cx_cube(A,B)

B.zeros()
B.set_size(10,10,10)
B.ones(5,6,7)

B.print("B:")

# Operations
A = cube(5, 10, 15, fill_randu)
B = cube(5, 10, 15, fill_randu)
C = cube(5, 10, 15, fill_randu)

P = A + B
Q = A - B
R = -B
S = A / 123.0
T = A / B
U = A @ C

AA = ucube([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]])
BB = ucube([[[3, 2, 1], [6, 5, 4], [9, 8, 7]], [[3, 2, 1], [6, 5, 4], [9, 8, 7]]])

# compare elements
ZZ = (AA >= BB)

# broadcasting
X = cube(6, 5, 4, fill_ones)
v = cube(6, 5, 1, fill_randu)

# in-place addition of v to each column vector of X
X += v

# generate Y by adding v to each column vector of X
Y = X + v 

# attributes
X = cube(4,5,6)
print("X has " + str(X.n_cols) + " columns")

# indexing
A = cube(10, 10, 10, fill_randu)
# A[9,9,9] = 123.0
# x = A[9,9,9]
# y = A[99]

# element initialisation
# v = cube([ 1, 2, 3 ])
# A = cube([ [1, 3, 5],
#           [2, 4, 6] ])

# member zeros
A = cube(5,10,15)
A.zeros()   
# or:  A = cube(5,10,fill_zeros)

B = cube()
B.zeros(10,20,30)

C = cube()
# C.zeros( size(B) )

# member ones
A = cube(5,10,15)
A.ones()
# or:  A = cube(5,10,fill_ones)

B = cube()
B.ones(10,20,30)

C = cube()
# C.ones( size(B) )

# randu/randn
A = cube(5,10,15)
A.randu()
# or:  A = cube(5,10,fill_randu)

B = cube()
B.randu(10,20,30)

C = cube()
# C.randu( size(B) )

# set_seed_random()  # set the seed to a random value

# fill
A = cube(5, 6, 7)
A.fill(123.0)
# A.fill(123) is also accepted and has the same result
A = cube(5, 6, 7, fill_zeros)

# clean
A = cube()

A.randu(1000, 1000, 1000)

# A[12,34] =  datum.eps
# A[56,78] = -datum.eps

# A.clean(datum.eps)

# replace
A = cube(5, 6, 7, fill_randu)

# A.fill(datum.nan)
A.fill(1)

# A.replace(datum.nan, 0) # replace each NaN with 0
A.replace(1, 0)

# set_size
A = cube()
A.set_size(5,10,15)       # or:  A = cube(5,10,15)

B = cube()
# B.set_size( size(A) )  # or:  B = cube( size(A) )

# reshape
A = cube(4, 5, 6, fill_randu)

A.reshape(6,5,4)

# resize
A = cube(4, 5, 6, fill_randu)

A.resize(7,6,5)

# copy_size

A = cube(5, 6, 7, fill_randu)
B = cube()
B.copy_size(A)

# reset
A = cube(5, 5, 5, fill_randu)
A.reset()

print(str(B.n_rows))
print(str(B.n_cols))
print(str(B.n_slices))

# reset
A = cube(5, 5, 5, fill_randu)
A.reset()

# subcube
A = cube(5, 10, 15, fill_zeros)

A[ 0:2, 1:3 , 2:4]             = cube(3,3,3, fill_randu)
A[ span(0,2), span(1,3), span(2,4) ] = cube(3,3,3, fill_randu)
# A[ 0,1, size(3,3) ]       = cube(3,3, fill_randu)

B = A[ 0:2, 1:3, 2:4].eval()
C = A[ span(0,2), span(1,3), span(2, 4) ].eval()
# D = A[ 0,1, size(3,3) ].eval()

# A[:,:,1]          = cube(5,5,1,fill_randu)
# A[span_all, span_all, 1]  = cube(5,5,1,fill_randu)

X = cube(5, 5, 5, fill_randu)

# get all elements of X that are greater than 0.5
# q = X[ find(X > 0.5) ]

# add 123 to all elements of X greater than 0.5
# X[ find(X > 0.5) ] += 123.0

# set four specific elements of X to 1
# indices = ucube([ 2, 3, 6, 8 ])

# X[indices] = cube(4,4,1,fill_ones)

# set_real, set_imag
A = cube(4, 5, 6, fill_randu)
B = cube(4, 5, 6, fill_randu)

C = cx_cube(4, 5, 6, fill_zeros)

C.set_real(A)
C.set_imag(B)

# fast cx_mat
A = cube(4, 5, 6, fill_randu)
B = cube(4, 5, 6, fill_randu)

# C = cx_cube(A,B)

# ins_row/cols
A = cube(5, 10, 15, fill_randu)
B = cube(5,  2, 15, fill_ones)

# at column 2, insert a copy of B;
# A will now have 12 columns
A.insert_cols(2, B)

# at column 1, insert 5 zeroed columns;
# B will now have 7 columns
B.insert_cols(1, 5)

# shed_row/cols
A = cube(5, 10, 15, fill_randu)
B = cube(5, 10, 15, fill_randu)

A.shed_row(2)
A.shed_cols(2,4)
A.shed_slices(4,6)

# indices = umat([4, 6, 8])
# B.shed_cols(indices)

# swap
A = cube(4, 5, 6, fill_zeros)
B = cube(6, 7, 8, fill_ones )

A.swap(B)

# iterators
X = cube(5, 6, 7, fill_randu)

for i in X:                # this prints all elements
  print(i)

it = iter(X)               # this also prints all elements
for i in it:
  print(i)

slice_it = slice_iter(X, 1, 3) # start of slice 1 and end of slice 3

for i in slice_it:
  print(i)

# iterators for subcubes


#max
A = cube(5, 5, 5, fill_randu)

max_val = A.max()

#ind_max
A = cube(5, 5, 5, fill_randu)

i = A.index_max()

# max_val = A[i]

#eval
# A = ucube(4,4,4,fill_ones)
A = cube(6,6,6,fill_ones)

# Any change to B does not affect A
B = A[0:1, 2:3, 4:5].eval()

# B[0,0,0] = 5

# Therefore, B and A[0:1, 2:3] should not be equal
# (B == A[0:1, 2:3]).print()

#in_range
A = cube(4, 5, 6, fill_randu)

print(A.in_range(0,0,0))  # true
print(A.in_range(3,4,5))  # true
print(A.in_range(4,5,6))  # false

#is_empty
A = cube(5, 5, 5, fill_randu)
print(A.is_empty())

A.reset()
print(A.is_empty())


#is_zero
A = cube(5, 5, 5, fill_zeros)

# A[0,0] = datum.eps

print(A.is_zero())
# print(A.is_zero(datum.eps))

#is_finite
A = cube(5, 5, 5, fill_randu)
B = cube(5, 5, 5, fill_randu)

B = cube(1,1,1)
# B[0,0,0] = datum.inf

print(A.is_finite())
print(B.is_finite())

#has_inf
A = cube(5, 5, 5, fill_randu)
B = cube(5, 5, 5, fill_randu)

B = cube(1,1,1)
# B[0,0,0] = datum.inf

print(A.has_inf())
print(B.has_inf())

#has_nan
A = cube(5, 5, 5, fill_randu)
A = cube(5, 5, 5, fill_randu)

B = cube(1,1,1)
# B[0,0,0]  = datum.nan

print(A.has_nan())
print(B.has_nan())

#print
A = cube(5, 5, 5, fill_randu)
A = cube(6, 6, 6, fill_randu)

A.print()

# "B:" is the optional header line
B.print("B:")

#save/load
A = cube(5, 6, 7, fill_randu)

# default save format is arma_binary
A.save("A.bin")

# save in raw_ascii format
A.save("A.txt", raw_ascii)

# save in CSV format without a header
A.save("A.csv", csv_ascii)

# save in HDF5 format
# A.save("A.h5", hdf5_binary)

# automatically detect format type while loading
B = cube()
B.load("A.bin")

# force loading in arma_ascii format
C = cube()
C.load("A.txt", arma_ascii)

# example of testing for success
D = cube()
ok = D.load("A.bin")

if not ok:
  print("problem with loading")

# abs
A = cube(5, 5, 5, fill_randu)
B = abs(A) 

X = cx_cube(5, 5, 5, fill_randu)
Y = abs(X)

# accu
A = cube(5, 6, 7, fill_randu)
B = cube(5, 6, 7, fill_randu)

x = accu(A)

# accu(A * B) is a "multiply-and-accumulate" operation
# as operator * performs element-wise multiplication in cube 

#approx_equal
A = cube(5, 5, 5, fill_randu)
B = A + 0.001

same1 = approx_equal(A, B, "absdiff", 0.002)

C = 1000 * cube(5,5,5, fill_randu)
D = C + 1

same2 = approx_equal(C, D, "reldiff", 0.1)

same3 = approx_equal(C, D, "both", 2, 0.1)

#arg
# A = cx_cube(5, 5, fill_randu)
B = arg(A)

#clamp
# A = cube(5, 5, 5, fill_randu )

# B = clamp(A, 0.2,     0.8) 

# C = clamp(A, A.min(), 0.8) 

# D = clamp(A, 0.2, A.max()) 

#find
A = cube(5, 5, 5, fill_randu)
A = cube(5, 5, 5, fill_randu)

# q1 = find(A > B)
# q2 = find(A > 0.5)
# q3 = find(A > 0.5, 3, "last")

# change elements of A greater than 0.5 to 1
# A[ find(A > 0.5) ].ones()

#find_finite
A = cube(5, 5, 5, fill_randu)

# A[1,1,1] = datum.inf

# accumulate only finite elements
# val = accu( A[ find_finite(A) ] )

#find_nonfinite
A = cube(5, 5, 5, fill_randu)

# A[1,1,1] = datum.inf
# A[2,2,2] = datum.nan

# change non-finite elements to zero
# A[ find_nonfinite(A) ].zeros()

#find_unique
# A = cube([ [ 2, 2, 4 ], 
#           [ 4, 6, 6 ] ])

# indices = find_unique(A)

#ind2sub
# Q = cube(4, 5, 6, fill_randu)

# s = ind2sub( size(Q), 6 )

# print("row: " + str(s[0]))
# print("col: " + str(s[1]))


# indices = find(Q > 0.5)
# t       = ind2sub( size(Q), indices )

#index_min/max

# v = cube(10, 5, 1, fill_randu)

# i = index_max(v)
# max_val_in_v = v[i]


# Q = cube(5, 6, 7, fill_randu)

# ii = index_max(Q)
# jj = index_max(Q,1)

# max_val_in_col_2 = Q[ ii[2], 2 ]

# max_val_in_row_4 = Q[ 4, jj[4] ]

#join
A = cube(4, 5, 6, fill_randu)
B = cube(4, 5, 5, fill_randu)

AB = join_slices(A,B)

#max
v = cube(10, 5, 1, fill_randu)
x = max(v)

Q = cube(10, 10, 10, fill_randu)

a = max(Q)
b = max(Q,0) 
c = max(Q,1)

# element-wise maximum
# X = cube(5, 6, 7, fill_randu)
# Y = cube(5, 6, 7, fill_randu)
# Z = max(X,Y)

#reshape
A = cube(10, 5, 1, fill_randu)

B = reshape(A, 1, 5, 10)

#resize
A = cube(4, 5, 6, fill_randu)

B = resize(A, 7, 6, 5)

#size
# A = cube(5,6,7)

# B = cube(size(A), fill_zeros)

# C = cube()

# C.randu(size(A))

# D = cube(10,20, fill_ones)
# D[3,4,size(C)] = C    # access submatrix of E

# E = cube( size(A) + size(E) )
# G = cube( size(A) * 2 )
# print("size of A: " + str(size(A)))
# is_same_size = (size(A) == size(E))

#sum
Q = cube(10, 10, 10, fill_randu)

a = sum(Q)
b = sum(Q,0)
c = sum(Q,1)

y = accu(Q)   # find the overall sum regardless of object type

#sub2ind
Q = cube(4,5,6)

# i = sub2ind( size(Q), 2, 3 )

#exp
A = cube(5, 5, 5, fill_randu)
B = exp(A)

#cos
X = cube(5, 5, 5, fill_randu)
Y = cos(X)

#stats
A = cube(5, 5, 5, fill_randu)

B = mean(A)
m = mean(mean(A))

#const
# print("2.0 * pi = " + str(2.0 * datum.pi))

# print("speed of light = " + str(datum.c_0))

# #print("log_max for floats = " + str(fdatum.log_max))

# print("log_max for doubles = " + str(datum.log_max))
